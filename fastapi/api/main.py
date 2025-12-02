from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from .routers import auth, workouts, routines

from .database import Base, engine
=======
from api.routers import auth, workouts, routines

from api.database import Base, engine
>>>>>>> 06f716055b3c6dd1cc385fbd15a6aa910770b7e9

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def health_check():
    return 'Health check complete'

app.include_router(auth.router)
app.include_router(workouts.router)
<<<<<<< HEAD
app.include_router(routines.router)
=======
app.include_router(routines.router)
>>>>>>> 06f716055b3c6dd1cc385fbd15a6aa910770b7e9
