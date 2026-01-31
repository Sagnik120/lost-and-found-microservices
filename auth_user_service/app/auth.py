from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def mask_email(email: str) -> str:
    name, domain = email.split("@")
    if len(name) <= 2:
        masked = name[0] + "****"
    else:
        masked = name[:2] + "****"
    return masked + "@" + domain
