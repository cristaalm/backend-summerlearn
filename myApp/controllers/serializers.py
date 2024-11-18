from rest_framework import serializers
from myApp.models import UserData, Status, Rol
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import hashlib
import os

def generate_key(passphrase: str) -> bytes:
    # Hash the passphrase to create a 256-bit (32 bytes) key
    return hashlib.sha256(passphrase.encode()).digest()


# Function to encrypt text
def encrypt(plain_text: str, passphrase: str) -> str:
    key = generate_key(passphrase)
    iv = os.urandom(16)  # Generate a random initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plain text to be a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()

    # Encrypt the data
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    # Return the base64 encoded string of the iv and encrypted data
    return base64.b64encode(iv + encrypted).decode('utf-8')

# Function to decrypt text
def decrypt(encrypted_text: str, passphrase: str) -> str:
    key = generate_key(passphrase)
    # Decode the base64 encoded string
    data = base64.b64decode(encrypted_text.encode('utf-8'))

    # Extract the IV from the beginning of the data
    iv = data[:16]
    encrypted_data = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_text = unpadder.update(padded_data) + unpadder.finalize()

    return plain_text.decode('utf-8')

class DecryptSerializer(serializers.Serializer):
    encrypted_text = serializers.CharField(max_length=255)
    # passphrase = serializers.CharField(max_length=255)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Llamar al método `get_token` del padre para obtener el token
        token = super().get_token(user)

        # Añadir datos personalizados al token
        token['username'] = user.name
        token['rol'] = user.users_rol.rol_id
        token['status'] = user.users_status.status_id

        return token



########################################################################################
# Define un serializer basado en el modelo 'UserData'.
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'
        read_only_fields = ('id',)


########################################################################################
# Define un serializer basado en el modelo 'UserData'.
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserData
        fields = ['name', 'first_name','last_name','email', 'password', 'users_photo', 'users_birthdate', 'users_phone', 'users_rol', 'users_status', 'users_tour']
    
    def create(self, validated_data):
        # Extract the password from validated data
        password = validated_data.pop('password')
        
        # Create the user with the rest of the validated data
        user = UserData(**validated_data)
        
        # Hash the password
        user.password = make_password(password)
        
        # Save the user
        user.save()
        
        return user


########################################################################################

# Define un serializer basado en el modelo 'Status'.
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status  # Define el modelo que será serializado.

        fields = '__all__'
        # Lista los campos del modelo 'User' que serán serializados.

        read_only_fields = ('status_id',)


########################################################################################
# Define un serializer basado en el modelo 'Rol'.
class RolSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Rol

        fields = '__all__'

        read_only_fields = ('rol_id',)