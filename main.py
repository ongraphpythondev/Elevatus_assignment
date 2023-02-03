from fastapi import FastAPI
from routers.user import user_router
from routers.candidate import candidate_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(user_router)
app.include_router(candidate_router)