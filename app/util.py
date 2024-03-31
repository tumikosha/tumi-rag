import hashlib
from collections import defaultdict
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import SparseVector
import uuid


def string_to_uuid4(input_string):
    # Convert string to UUID4
    hashed = hashlib.md5(input_string.encode('utf-8')).hexdigest()
    uuid_obj = uuid.UUID(f"{hashed[:8]}-{hashed[8:12]}-4{hashed[13:16]}-{hashed[16:20]}-{hashed[20:32]}")
    return str(uuid_obj)


def to_valid_uuid4(input_string):
    if not is_valid_uuid(input_string):
        return string_to_uuid4(input_string)
    return input_string


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
