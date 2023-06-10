from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    BlogListCreateAPIView,
    BlogRetrieveUpdateDestroyAPIView,
    LoginAPIView,
    LogoutAPIView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("blogs/", BlogListCreateAPIView.as_view(), name="blog-list-create"),
    path(
        "blogs/<int:pk>/",
        BlogRetrieveUpdateDestroyAPIView.as_view(),
        name="blog-retrieve-update-destroy",
    ),
]
