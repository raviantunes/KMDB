from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import User
from .serializers import UserSerializer, LoginSerializer


class UserView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.is_superuser == 1:
            pass
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status.HTTP_401_UNAUTHORIZED)

        users = User.objects.all()
        result_page = self.paginate_queryset(users, request, view=self)

        serializer = UserSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class UserViewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.is_superuser == 1:
            pass
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


class UserRegisterView(APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except AssertionError:
            return Response({"detail": "invalid email or password"}, status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data, status.HTTP_200_OK)
