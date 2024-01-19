import datetime
import traceback
from django.http import JsonResponse
import pytz
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework import status
from .helpers import createResponse, decrypt_AES_CBC, encrypt_AES_CBC
from Crypto.Random import get_random_bytes
from .validations import register_user_validator,user_authenticate_validator,param_validator
from .models import UserProfile
from .authentication import ExpiringTokenAuthentication
from .utils import generate_jwt_token
from rest_framework.permissions import IsAuthenticated
from .utils import CustomJWTAuthentication
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry



cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"

error_string = "Something seems to have  gone wrong. Try again later?"


@authentication_classes([ExpiringTokenAuthentication])
@api_view(['POST'])
def registerUser(request):
    try:
        data = request.data
        is_valid, message, validatedData = register_user_validator(data=data)
        if not is_valid:
            return createResponse(status.HTTP_406_NOT_ACCEPTABLE, message)
        
        try:
            existing_name=list(UserProfile.objects.filter(username=validatedData.get('username')).values())  
            if len(existing_name) > 0:
                message = {"message": "Username already exist with same name .", "status": 406}
                return JsonResponse(message, status=status.HTTP_406_NOT_ACCEPTABLE)             
        except Exception as e:
            print(traceback.format_exc()) 
            return createResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, f'Unable to register user.{error_string}')    

        else:
            encrypt_password = encrypt_AES_CBC(validatedData.get('password'))
            user = UserProfile.objects.create(username=validatedData.get('username'), password=encrypt_password)
            user.save()
            return createResponse(status.HTTP_201_CREATED, 'User registered successfully.', payload=validatedData)
    except Exception as error:
        print(traceback.format_exc()) 
        return createResponse(status.HTTP_400_BAD_REQUEST, f'Unable to register user.{error_string}')  
    

@api_view(['POST'])
def userAuthentication(request):
        try:
            data=request.data

            is_valid, message, validatedData = user_authenticate_validator(data)
            if not is_valid:
                return createResponse(status.HTTP_406_NOT_ACCEPTABLE, message)

            username = validatedData.get('username')
            password = validatedData.get('password')

            existing_user_obj = UserProfile.objects.filter(username=username,).values()
            if not existing_user_obj:
                return createResponse(status.HTTP_401_UNAUTHORIZED,'User does not exist. Please register before log in.')
            
            else:
                existing_password=existing_user_obj[0].get('password')
                existing_username=existing_user_obj[0].get('username')
                user =existing_user_obj[0].get("id")
            
                decrypt_pass = decrypt_AES_CBC(existing_password)
                if username==existing_username and password==decrypt_pass:
                    utc_now=datetime.datetime.now()
                    utc_now=utc_now.replace(tzinfo=pytz.utc)

                    token = generate_jwt_token(user)
                    print(token)   
            
                    return createResponse(status.HTTP_200_OK,token)

                return createResponse(status.HTTP_401_UNAUTHORIZED,'Invalid credentials')
        except Exception as error:
            print(traceback.format_exc()) 
            return createResponse(status.HTTP_401_UNAUTHORIZED, f'Unable to authenticate user.{error_string}') 
        

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    A protected view that requires a valid JWT token for access.
    """
    user = request.data 
    return createResponse(status.HTTP_202_ACCEPTED,'Authorisation provide.')




@api_view(['POST'])
def getHourlyData(request):
        hourly=["temperature_2m", "precipitation", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"]

        try:
            data=request.data

            is_valid, message, validatedData = param_validator(data)
            if not is_valid:
                return createResponse(status.HTTP_406_NOT_ACCEPTABLE, message)
            
            data["hourly"]=["temperature_2m", 
                            "precipitation", 
                            "cloud_cover", 
                            "cloud_cover_low", 
                            "cloud_cover_mid", 
                            "cloud_cover_high"
                        ]

            responses = openmeteo.weather_api(url, params=data)

            response = responses[0]
            print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
            print(f"Elevation {response.Elevation()} m asl")
            print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
            print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
            hourly_cloud_cover = hourly.Variables(2).ValuesAsNumpy()
            hourly_cloud_cover_low = hourly.Variables(3).ValuesAsNumpy()
            hourly_cloud_cover_mid = hourly.Variables(4).ValuesAsNumpy()
            hourly_cloud_cover_high = hourly.Variables(5).ValuesAsNumpy()

            hourly_data = {"date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s"),
                end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            )}
            hourly_data["temperature_2m"] = hourly_temperature_2m
            hourly_data["precipitation"] = hourly_precipitation
            hourly_data["cloud_cover"] = hourly_cloud_cover
            hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
            hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
            hourly_data["cloud_cover_high"] = hourly_cloud_cover_high

            hourly_dataframe = pd.DataFrame(data = hourly_data)
            
            return createResponse(status.HTTP_200_OK,"Get_hourly_data",payload=hourly_dataframe)

        except Exception as error:
            print(traceback.format_exc()) 
            return createResponse(status.HTTP_404_NOT_FOUND, f'{error_string} Unable to find weather data hourly.') 
       






 
