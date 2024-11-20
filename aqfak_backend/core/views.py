from core.utility import capitalizeDict
from user_auth.models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Crop, CropSensorData,CropSchedule
from .serializers import CropSerializer, CropSensorDataSerializer,CropScheduleSerializer
from django.db import transaction

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_create_crop(request):
    try:
        custom_user = request.user 
    except CustomUser.DoesNotExist:
        return Response({"detail": "User does not exist"}, status=404)

    if request.method == "GET":
        crops = Crop.objects.filter(user=custom_user)
        
        crop_serializer = CropSerializer(crops, many=True)
        crop_data = []

        for crop in crop_serializer.data:
            crop_instance_id = crop['id'] 
            sensor_data_instance = CropSensorData.objects.filter(crop_id=crop_instance_id).first()
            
            if sensor_data_instance:
                condition = CropSensorDataSerializer(sensor_data_instance).data.get('condition')
            else:
                condition = None

            crop['condition'] = condition
            crop_data.append(capitalizeDict(crop)) 

        return Response(crop_data, status=200)

    elif request.method == 'POST':
        try:
            crops = request.data.get('crops', [])
            
            if not crops:
                return Response({"detail": "No crops provided"}, status=400)
            
            created_crops = []
            
            with transaction.atomic(): 
                for crop in crops:
                    crop_record = Crop.objects.create(
                        user=custom_user,
                        name=crop['crop'],
                        stage=crop['stage'],
                        area=crop['area']
                    )
                    created_crops.append(crop_record)

            created_crops_serializer = CropSerializer(created_crops, many=True)
            
            return Response({"data": created_crops_serializer.data, "message": "Crops created successfully"}, status=201)

        except Exception as e:
            return Response({"detail": f"Error creating crops: {str(e)}"}, status=500)
        


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def retrieve_update_delete_crop(request, id):
    try:
        custom_user = request.user  
    except CustomUser.DoesNotExist:
        return Response({"detail": "User does not exist"}, status=404)

    try:
        crop = Crop.objects.get(id=id, user=custom_user)
    except Crop.DoesNotExist:
        return Response({"error": "Crop not found."}, status=404)

    if request.method == "GET":
        crop_serializer = CropSerializer(crop)
        return Response(crop_serializer.data, status=200)

    elif request.method == "PUT":
        data = {
            "name": request.data.get('name', crop.name),
            "area": request.data.get('area', crop.area),
            "stage": request.data.get('stage', crop.stage),
        }
        
        crop_serializer = CropSerializer(crop, data=data, partial=True)
        
        if crop_serializer.is_valid():
            crop_serializer.save()
            return Response(crop_serializer.data, status=200)
        else:
            return Response({'detail': crop_serializer.errors}, status=400)

    elif request.method == "DELETE":
        crop.delete()
        return Response({'detail': 'Crop deleted successfully'}, status=204)
    
@api_view(['POST'])
def create_crop_sensor_data(request,id):
    try:
        # Extract crop_id and sensor data from request
        crop_id = id
        condition = request.data.get('condition', 'normal')
        ph = request.data.get('ph')
        ph_status = request.data.get('phStatus', 'optimal')
        nitrogen = request.data.get('nitrogen')
        phosphorous = request.data.get('phosphorous')
        potassium = request.data.get('potassium')

        # Check if the crop exists
        try:
            crop = Crop.objects.get(id=crop_id)
        except Crop.DoesNotExist:
            return Response({"error": "The referenced crop does not exist."}, status=404)

        # Create CropSensorData instance
        sensor_data = CropSensorData.objects.create(
            crop=crop,
            condition=condition,
            ph=ph,
            phStatus=ph_status,
            nitrogen=nitrogen,
            phosphorous=phosphorous,
            potassium=potassium
        )

        # Serialize and return the created sensor data
        sensor_data_serializer = CropSensorDataSerializer(sensor_data)
        return Response(sensor_data_serializer.data, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)