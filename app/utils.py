
from passlib.context import CryptContext

# here we are telling passlib what is the default algorithm we want to use. Here it is bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
