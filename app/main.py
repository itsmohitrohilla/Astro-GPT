from fastapi import FastAPI
from app.database.db import engine, Base
from app.routers import user_router
from app.routers.astro_router import router as astro_router

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Astro-GPT")

app.include_router(user_router.router, tags = ["Create Astro User"])
app.include_router(astro_router, tags = ["Astro-GPT"])

# app.include_router(llm_routes.router,tags = ["Astro-GPT"])

