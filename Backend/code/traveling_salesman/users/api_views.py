from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


User = get_user_model()


@authentication_classes([])
@permission_classes([])
class RegisterUser(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([])
@permission_classes([])
class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })

@authentication_classes([])
@permission_classes([])
class Logout(GenericAPIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
