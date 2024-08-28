import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (ExpiredSignatureError, InvalidTokenError):
        return "error"
    except Exception as e:
        # Log the unexpected error
        print(f"Unexpected error decoding token: {str(e)}")
        return None