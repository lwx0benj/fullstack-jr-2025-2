from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.auth import auth

app = FastAPI()
app.include_router(auth)

origins = [
    'http://localhost:3000',
]

# Adicione o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Permite o envio de credenciais
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=['*'],  # Permite todos os cabeçalhos
)
