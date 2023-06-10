from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AuthUsers, Blog
from .serializers import (
    BlogSerializer,
    LoginSerializers,
    LogoutSerializer,
    RegisterSerializer,
)


class RegisterView(generics.GenericAPIView):
    """
    Register a new user and send email to user for verification of email address

    """

    serializer_class = RegisterSerializer

    def post(self, request):
        if AuthUsers.objects.filter(email=request.data["email"]).exists():
            return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Email already exists",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            user = request.data
            serializer = RegisterSerializer(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "User is created Please verify your email to login",
                },
                status=status.HTTP_201_CREATED,
            )


class LoginAPIView(generics.GenericAPIView):
    """
    Login user and return access, refresh and user details
    """

    serializer_class = LoginSerializers

    def post(self, request):
        serializers = self.serializer_class(data=request.data)

        serializers.is_valid(raise_exception=True)
        return Response(
            {
                "status_code": status.HTTP_200_OK,
                "message": "User Logged in",
                "data": serializers.data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(generics.GenericAPIView):
    """
    Logout user
    """

    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"status_code": status.HTTP_200_OK, "message": "Logout Successfully"},
            status=status.HTTP_200_OK,
        )


class BlogListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = Blog.objects.filter(user=request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        user_instance = AuthUsers.objects.filter(id=request.auth["user_id"]).first()
        if serializer.is_valid():
            serializer.save(user=user_instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BlogRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk, user=self.request.auth["user_id"])
        except Blog.DoesNotExist:
            raise NotFound("Blog not found.")

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=204)
