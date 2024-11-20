from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from .models import CustomUser  # Import your CustomUser model
from .serializers import CustomUserSerializer  # Import your serializer
from django.contrib.auth.models import User

@api_view(['POST'])
def signup(request):
    try:
        user_info = request.data.get('userInfo')
        
        if not user_info:
            return Response({'detail': 'userInfo is missing'}, status=400)
        
        required_fields = ['userId', 'nickname', 'photo', 'place']
        for field in required_fields:
            if field not in user_info:
                return Response({'detail': f'{field} is missing'}, status=400)

        if CustomUser.objects.filter(email=user_info["userId"]).exists():
            return Response({'detail': 'A user with this email already exists'}, status=400)

        custom_user = CustomUser.objects.create_user(
            username=user_info["userId"],  # Assuming userId is used as the username
            email=user_info["userId"],     # Assuming email is the same as userId (adjust as needed)
            name=user_info["nickname"],
            profilePhoto=user_info["photo"],
            place=user_info["place"]
        )
        
        custom_user.save()

        token, created = Token.objects.get_or_create(user=custom_user)

        custom_user_serializer = CustomUserSerializer(custom_user)

        return Response({
            'data': custom_user_serializer.data,
            'token': token.key 
        }, status=201)

    except IntegrityError as e:
        return Response({'detail': 'Integrity error occurred', 'exception': str(e)}, status=400)
    except KeyError as e:
        return Response({'detail': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        return Response({'detail': 'Something went wrong', 'exception': str(e)}, status=500)
    


@api_view(['POST'])
def signin(request):
    user_id = request.data.get("user_id")
    
    try:
        user = CustomUser.objects.get(username=user_id)
        
        custom_user_serializer = CustomUserSerializer(user)
        
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'msg': 'true',
            'data': custom_user_serializer.data,
            'token': token.key
        }, status=200)

    except CustomUser.DoesNotExist:
        return Response({'msg': 'false', 'detail': 'User not found'}, status=404)
    except Exception as e:
        return Response({'msg': 'false', 'detail': str(e)}, status=500)

@api_view(['GET'])
def signout(request):
    try:
        request.user.auth_token.delete()
        return Response({'detail':'Successfully logged out'})
    except Exception as e :
        return Response({'detail': f'Something went wrong'})


# @api_view(['GET','PUT','DELETE'])
# @permission_classes([IsAuthenticated])
# def retrieve_update_user(request):
#     try:
#         # user= User.objects.get(username='vus09003@gmail.com')
#         custom_user=CustomUser.objects.get(user=request.user)
#         if request.method == 'GET':
#             user_serializer = CustomUserSerializer(custom_user)
#             return Response({"user":user_serializer.data})
        
#         elif request.method == 'PUT':
#             user_serializer = CustomUserSerializer(custom_user,data=request.data,partial=True)
#             if user_serializer.is_valid():
#                 user_serializer.save()
#             else:
#                 return Response({'detail': user_serializer.errors})
#             return Response({"user":user_serializer.data})
#         elif request.method == 'DELETE':
#             if custom_user:
#                 custom_user.delete()
#                 return Response('deleted')
                
#     except Exception as e:
#         return Response({'detail': f'Something went wrong', 'exception': str(e)})

#



        



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getcrop_details(request) :
#     custom_user = CustomUser.objects.get(user=request.user)
#     crop = request.GET.get('crop')

#     #getting instances
#     cropInstance = Crop.objects.get(user=custom_user,name=crop )
#     sensorData = {}
#     try:
#         sensorDataInstance = CropSensorData.objects.get(crop=cropInstance)
#         sensorData = CropSensorDataSerializer(sensorDataInstance, many=False).data
#         sensorData['npk'] = [                  
#             sensorData.pop('nitrogen'),
#             sensorData.pop('phosphorous'),
#             sensorData.pop('potassium'),
#         ]
#         sensorData['id'] = sensorData.pop('crop') #replacing the primary key of sensor data with its foreign key crop.As they are onetoone relation, it shouldnt be a problem    

#     except CropSensorData.DoesNotExist:
#         sensorData = {}
     
    
#     #getting data from instances
#     crop = CropSerializer(cropInstance, many=False).data
#     scheduleInstances = CropSchedule.objects.filter(crop = cropInstance)
#     schedule = CropScheduleSerializer(scheduleInstances, many=True).data if scheduleInstances else []

#     #merging separte columns of nitrogen ,phosphorous and potassium together
       
#     #putting everything together
#     crop.update(sensorData)
#     crop = capitalizeDict(crop)
#     crop['schedule'] = capitalizeDict(schedule)

#     return Response(crop)

















