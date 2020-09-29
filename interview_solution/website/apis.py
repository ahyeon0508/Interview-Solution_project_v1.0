from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User
from .serializers import SignupUserSerializer

# Create your api here.

@api_view(['POST'])
def signup(request):
    if request.method == "POST":
        serializer = SignupUserSerializer(data = request.data)
        if(serializer.validated_data['password']!=serializer.validated_data['passwordChk']):
            return Response({"message":"Password Error"})