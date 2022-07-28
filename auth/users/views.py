from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime

from rest_framework import authentication, exceptions

class RegisterView(APIView):
    def post(self, request):
        print(request)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if len(request.data['password']) >= 8:
            serializer.save()
        else:
            raise AuthenticationFailed('Password must be at least 8 characters!')

        token = jwt.encode(serializer.data, 'secret', algorithm='HS256')#.decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50000),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')#.decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    authentication_header_prefix = 'Bearer'
    def get(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
     
        if not auth_header:
            raise AuthenticationFailed('Unauthenticated!')

        if len(auth_header) == 1:
            raise AuthenticationFailed('Unauthenticated!')

        elif len(auth_header) > 2:
            raise AuthenticationFailed('Unauthenticated!')

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'isSuccessful': True
        }

        return response

