from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from got.serializer import *
from got.emails import *

from django.http import JsonResponse




def register_page(request):
    return render(request, 'index.html')

class RegisterAPI(APIView):
    
    def post(self,request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status' : 200,
                    'message' : 'register successfully check email.',
                    'data' : serializer.data,
                
            })
                    
            return Response({
                'status' : 400,
                'message' : 'something went wrong.',
                'data' : serializer.errors
            })
            
        except Exception as e:
            print(e)
            
            
            
            
class VerifyOTP(APIView):
    def post(self,request):
        try:
            data = request.data
            serializers = VerifyAccountSerializer(data=data)
            
            if serializers.is_valid():
                email = serializers.data['email']
                otp = serializers.data['otp']
                
                user = User.objects.filter(email=email)
                if not user.exists():  
                    return Response({
                        'status' : 400,
                        'message' : 'something went wrong.',
                        'data' : 'invaild email'

                })
                    
                if not user[0].otp == otp:
                    return Response({
                        'status' : 400,
                        'message' : 'something went wrong.',
                        'data' : 'wrong otp'

                    })
                    
                user = user.first()
                user.is_verified = True
                user.save()
                
                return Response({
                    'status' : 200,
                    'message' : 'account verified',
                    'data' : {},
                
                })
                    
            return Response({
                'status' : 400,
                'message' : 'something went wrong.',
                'data' : serializers.errors
            })
        
            
        except Exception as e:
            print(e)
