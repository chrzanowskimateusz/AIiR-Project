from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer

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
