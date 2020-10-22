from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from .serializers import VerificationSerializer
from .verification import verify
from .permissions import IsNotVerified, HasNotActiveVerification


class BaseGenerateVerificationAPIView(generics.GenericAPIView):
    send_code_function = None
    serializer_class = VerificationSerializer
    permission_classes = [IsAuthenticated, IsNotVerified, HasNotActiveVerification]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        self.send_code_function(reuest=request, **serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class BaseVerifyVerificationAPIView(generics.GenericAPIView):
    serializer_class = VerificationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verified = verify(**serializer.validated_data)
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
