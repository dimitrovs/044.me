import datetime
import jwt
import config


def decode(token: str):
    return jwt.decode(
        token, config.SECRET_KEY, algorithms=[config.ALGORITHM])


def encode(user_id: str, ):
    return jwt.encode({
        "id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
    }, config.SECRET_KEY, config.ALGORITHM)
