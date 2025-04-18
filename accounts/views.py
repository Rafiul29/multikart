from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import UserRegistrationSerializer
from rest_framework import status, permissions

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            user = serializer.save()
            tokens = self.get_tokens_for_user(user)  # generate the JWT token
            return Response({"message": "User registered successfully!", "tokens": tokens}, status=status.HTTP_201_CREATED)
        
        # modify the error response
        errors = {}
        for field, error in serializer.errors.items():
            if isinstance(error, list):
                errors[field] = error[0] if isinstance(error[0], str) else str(error[0])

        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
    


class LoginApiView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # generate error response 
        if not username or not password:
            errors = {}
            if not username:
                errors["username"] = "Username is required."
            if not password:
                errors["password"] = "Password is required."

            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "please provided valid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        
        login(request,user)
        tokens = self.get_tokens_for_user(user)

        data = {
              "id":user.id,
              'first_name':user.first_name,
              'last_name':user.last_name,
              'username':user.username,
              'email':user.email,
              'role':user.role
            } 

        return Response({"message": "user login successful","data": data, "tokens": tokens})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

class LogoutApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if refresh_token is None:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)
