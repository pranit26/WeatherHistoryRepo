import json
from django.http import HttpRequest
from django.http.response import JsonResponse
import logging
from rest_framework.response import Response
from rest_framework import status
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from WeatherAPIProject.settings import ENC_KEY

logger = logging.getLogger(__name__)



def createResponse(status=status.HTTP_200_OK, message='Internal Server Error', payload=None, pager=None):
    if payload is None:
        payload = {}
    response = {'status': status, 'message': message}
    if len(payload):
        response['payload'] = payload
    if pager:
        response['pager'] = pager
    return Response(response, status=status)


def generate_key():    
    return get_random_bytes(16)  

def encrypt_AES_CBC(plaintext):
    iv = get_random_bytes(16)
    enc_key=ENC_KEY
    cipher = AES.new(enc_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(bytes(plaintext, 'utf-8'), AES.block_size))
    return f'{b64encode(iv).decode()}:{b64encode(ciphertext).decode()}'

def decrypt_AES_CBC(encrypted_text):
    enc_key=ENC_KEY
    iv, ciphertext = map(b64decode, encrypted_text.split(':'))
    print("enc_key-",enc_key,type(enc_key))
    cipher = AES.new(enc_key, AES.MODE_CBC, iv)
    decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_text.decode('utf-8')
