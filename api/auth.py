import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


def obtain_token_for_user(email, password):
    response = requests.post(
        'http://localhost:8000/api/token/',
        {"email": email, "password": password}
    )

    if response.status_code != 200:
        raise AuthenticationFailed("Incorrect credentials")

    tokens = response.json()

    return {
        'refresh': tokens['refresh'],
        'access': tokens['access'],
    }
