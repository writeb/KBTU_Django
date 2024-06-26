from passlib.context import CryptContext

from app.dramatiq_job import check_valid_name, result_backend
from dramatiq.results import Results, ResultMissing

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def is_valid_name(username: str):
    task = check_valid_name.send(username)
    return {'id': task.message_id}


def result(id: str):
    try:
        task = check_valid_name.message().copy(message_id=id)
        return result_backend.get_result(task)
    except ResultMissing:
        return "Waiting for all requests"