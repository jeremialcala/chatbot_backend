from functools import wraps
from constants import *
import time
import boto3


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        print(f'Starting {func.__name__}')
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} completed total time:{total_time:.4f} seconds')
        return result

    return timeit_wrapper


@timeit
def load_credentials():
    credentials = {}
    with open(".aws/credentials") as f:
        for line in f:
            key, value = line.strip().split("=")
            credentials[key] = value
        f.close()
    return credentials


@timeit
def load_env_variables(env_file="env_variables"):
    variables = {}
    with open(env_file) as vars_file:
        for line in vars_file:
            _key, _value = line.strip().split(" = ")
            variables[_key] = _value
        vars_file.close()
    return variables


@timeit
def create_session_session(credentials):
    if credentials is None:
        credentials = load_credentials()
    return boto3.Session(
        aws_access_key_id=credentials[aws_access_key_id],
        aws_secret_access_key=credentials[aws_secret_access_key],
        region_name=AWS_REGION
    )


@timeit
def get_queue(sqs, queue_name):
    queues = [_queue for _queue in sqs.queues.all()]
    return sqs.get_queue_by_name(chat_msg) if queue_name in queues else sqs.create_queue(QueueName=chat_msg,
                                                                                         Attributes=
                                                                                         {"DelaySeconds": "5"})
