from datetime import datetime, timedelta

from jose import JWTError, jwt  # type:ignore

secret_key = "123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def generate_token(id: int):
    to_encode: dict = {"id": id}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, secret_key, algorithm=ALGORITHM
    )
    return encoded_jwt

# пример декодера сразу с использованием
# def get_current_customer(
#         session: Session = Depends(get_session)
# ):
#     try:
#         payload = jwt.decode(
#             access_token, app_config.secret_key, algorithms=[ALGORITHM]
#         )
#         customer_id: int = payload.get("id")
#         customer = Customer(id=customer_id).db_read_by_id(session=session)
#         if customer is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Customer not found",
#             )
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#         )
#     return customer
