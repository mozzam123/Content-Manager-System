from .serializers import *
from .models import *
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        return JsonResponse({"Token": response}) 


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data
            response = {"status": "success", "data": "", "http_status": HTTP_201_CREATED} 
            serializer = CustomUserSerializer(data=data)

            if serializer.is_valid():
                # Hash the password before saving
                password = make_password(data.get('password'))
                serializer.validated_data['password'] = password

                # Save the user object
                user = serializer.save()
                response['status'] = "success"
                response["data"] = serializer.data
            else:
                response["status"] =   "error"
                response["http_status"] = HTTP_400_BAD_REQUEST
                response["data"] = serializer.errors

        except Exception as e:
            response["status"] = "error"
            response["http_status"] = HTTP_400_BAD_REQUEST
            response["data"] = str(e)

        return JsonResponse(response, status=response.get('http_status', HTTP_200_OK))
            

class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer

    def post(self, request):
        response = {"status": "success", "data": "", "http_status":HTTP_200_OK}

        # Extract email and password from the request data
        email = request.data.get("email")
        password = request.data.get("password")

        if email and password:  # Check if email and password are provided
            # Authenticate the user
            user = authenticate(request=request, username=email, password=password)

            if user is not None:
                # Login the user
                login(request, user)

                # Create or get a token for the user
                token, created = Token.objects.get_or_create(user=user)

                response['status'] = "success"
                response['data'] = "logged in successfully"
                response['token'] = token.key  # Include the token in the response
            else:
                response['status'] = "failed"
                response['data'] = "invalid credentials"
                response['http_status'] = HTTP_400_BAD_REQUEST
        else:
            response["status"] = "error"
            response["http_status"] = HTTP_400_BAD_REQUEST
            response["data"] = "email and password are required"

        return Response(response, status=response.get('http_status',HTTP_200_OK))



class CreateContentView(APIView):

    def post(self, request):
        response = {"status": "success", "data": "", "http_status": HTTP_201_CREATED}

        username = request.data.get('username')
        user_queryset = CustomUser.objects.filter(username=username)
        user = user_queryset.first()
        
        if user.role == 'author':
            serializer = CreateContentItemSerializer(data=request.data.get('content'))
            
            if serializer.is_valid():
               content_item  =  serializer.save(author = user)
               response["data"] = CreateContentItemSerializer(content_item).data
        else:
            response["status"] = "error"
            response["data"] = 'Only authors can create content'
            response['http_status'] = HTTP_400_BAD_REQUEST

        return JsonResponse(response, status=response["http_status"])
    


class GetAllContentView(APIView):
    def post(self, request):
        response = {"status": "success", "data": "", "http_status": HTTP_200_OK}
        username = request.data.get('username')
        user_queryset = CustomUser.objects.filter(username=username)
        user = user_queryset.first()

        if user is not None:
            if user.role == 'admin':

                query_set = ContentItem.objects.all()
                serializers = ContentItemSerializer(query_set, many=True)
                response['status'] = "success"
                response["data"] = serializers.data

            elif user.role == 'author':

                # Retrieve content items created by the author
                query_set = ContentItem.objects.filter(author=user)
                serializers = ContentItemSerializer(query_set, many=True)
                response['status'] = "success"
                response["data"] = serializers.data

        
        return JsonResponse(response, status=response.get('http_status', HTTP_200_OK))


class DeleteContentView(APIView):
    def post(self, request):
        try:
            response = {"status": "success", "data": "", "http_status": HTTP_200_OK}
            username = request.data.get('username')
            content_id = request.data.get("content_id")

            user_queryset = CustomUser.objects.filter(username=username)
            user = user_queryset.first()

            if user is not None:
                content_item = ContentItem.objects.get(content_id=content_id)
                
                if content_item is not None:
                    if user.role == 'admin' or user == content_item.author:
                        content_item.delete()
                        response["status"] = "success"
                        response["data"] = f"Content delete for {user.role}: {content_item}"

                    else:
                        response["status"] = "error"
                else:
                    response["status"] = "error"
                    response["data"] = "Content not found"
            else:
                response["status"] = "error"
                response["data"] = "user is not found"

        except Exception as e:
            response["status"] = "error"
            response["data"] = e

        return JsonResponse(response, status=response.get('http_status', HTTP_200_OK))



                    

class ContentItemSearchView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        response = {"status": "success", "data": "", "http_status": HTTP_200_OK}
        # Deserialize the search query
        serializer = ContentItemSearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']

            # Perform the search in the database
            content_items = ContentItem.objects.filter(
                title__icontains=query
            ) | ContentItem.objects.filter(
                body__icontains=query
            ) | ContentItem.objects.filter(
                summary__icontains=query
            ) | ContentItem.objects.filter(
                category__icontains=query
            )

            # Serialize the results and return them
            serializer = ContentItemSerializer(content_items, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)