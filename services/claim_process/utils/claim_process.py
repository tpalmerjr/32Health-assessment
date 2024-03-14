from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address

# The slowapi limiter
limiter = Limiter(key_func=get_remote_address)

# The FastAPI app
app = FastAPI()
