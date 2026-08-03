from django.shortcuts import get_object_or_404, render
from rest_framework.views import Response, APIView
from rest_framework.request import Request
from .serializers import UserSerializer, LoginSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.auth import authenticate
from .permissions import IsAdminOrEmployeeOrOwner

class UserView(APIView):
    def getPermissions(self):
        if self.request.method == "POST":
            return[AllowAny()]
        return [ISAuthenticated(), IsAdminOrEmployeeOrOwner()]
    
    def post(self, request:Request)->Response:
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request:Request)-> Response:
        users = User.object.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class LoginView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({"detail": "User account is not active"}, status.HTTP_403_FORBIDDEN)
        refresh = RefreshToken.for_user(user)
        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return Response(token_data, status.HTTP_200_OK)

class UserDetailView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrEmployeeOrOwner,)
    def get(self, request: Request, user_id:int)-> Response:
        found_user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, found_user)
        serializer = UserSerializer(found_user)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        found_user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, found_user)
        serializer = UserSerializer(found_user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

class PromoteUserView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    def patch(self, request: Request, user_id: int) -> Response:
        found_user = get_object_or_404(User, id=user_id)
        serializer = PromoteUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        found_user.is_employee = serializer.validated_data["is_employee"]
        found_user.save(update_fields = ["is_employee"])
        return Response(UserSerializer(found_user). data, status.HTTP_200_OK)
    