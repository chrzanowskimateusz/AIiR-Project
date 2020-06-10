from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import File, Result
from .serializers import FileSerializer, ResultSerializer, CalculatePathSerializer


class Results(GenericAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def get(self, request, *args, **kwargs):
        serialized = self.serializer_class(self.get_queryset(), many=True)
        return Response(serialized.data)


class UserResults(GenericAPIView):
    queryset = Result.objects
    serializer_class = ResultSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serialized = self.serializer_class(data, many=True)
        return Response(serialized.data)


class FileUpload(GenericAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        serialized = self.serializer_class(self.get_queryset(), many=True)
        return Response(serialized.data)


class CalculatePath(GenericAPIView):
    serializer_class = CalculatePathSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # result = calculate_path(serializer.data) not implemented
            serialized_result = ResultSerializer(data=result)
            if serialized_result.is_valid():
                serialized_result.save()
                return Response(serialized_result.data, status=status.HTTP_200_OK)
            return Response(serialized_result.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
