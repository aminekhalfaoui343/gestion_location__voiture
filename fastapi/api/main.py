from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, workouts, routines
from api.database import Base, engine

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/")
def health_check():
    return {"message": "Health check complete"}

# Routers
app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(routines.router)
