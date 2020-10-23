from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from .serializers import VerificationGenerateSerializer, VerificationVerifySerializer, \
    VerificationGenerateRequestSerializer
from .verification import verify
from .permissions import IsNotVerified, HasNotActiveVerification
from . import conf


class BaseAPIView(generics.GenericAPIView):
    request_serializer_class = None

    def get_request_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing request.
        """
        request_serializer_class = self.get_request_serializer_class()

        if request_serializer_class is None:
            request_serializer_class = self.get_serializer_class()
            kwargs['context'] = self.get_serializer_context()
        else:
            kwargs['context'] = self.get_request_serializer_context()

        return request_serializer_class(*args, **kwargs)

    def get_request_serializer_class(self):
        """
        Return the class to use for the request serializer.
        Defaults to using `self.request_serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        return self.request_serializer_class

    def get_request_serializer_context(self):
        """
        Extra context provided to the request serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }


class BaseGenerateVerificationAPIView(BaseAPIView):
    send_code_function = None
    request_serializer_class = VerificationGenerateRequestSerializer
    serializer_class = VerificationGenerateSerializer
    permission_classes = (IsAuthenticated, IsNotVerified, HasNotActiveVerification)

    def post(self, request, *args, **kwargs):
        request_serializer = self.get_request_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()
        response_serializer = self.get_serializer(
            instance=request_serializer.instance
        )
        headers = self.get_success_headers(response_serializer.data)
        self.send_code_function(request, request_serializer.instance)
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK, headers=headers
        )

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class BaseVerifyVerificationAPIView(generics.GenericAPIView):
    serializer_class = VerificationVerifySerializer
    permission_classes = (IsAuthenticated, IsNotVerified)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance
        data = serializer.validated_data
        data[conf.VERIFICATION_CODE_FIELD] = getattr(instance, conf.VERIFICATION_CODE_FIELD)
        verified = verify(**data)
        response_data = {}
        if not verified:
            response_data['verified'] = verified
            return Response(response_data, status=status.HTTP_200_OK)
        headers = self.get_success_headers(serializer.data)
        response_data.update(serializer.data)
        response_data['verified'] = verified
        return Response(response_data, status=status.HTTP_200_OK, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
