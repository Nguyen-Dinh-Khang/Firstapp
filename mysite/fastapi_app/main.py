import os
import django
from fastapi import FastAPI
from fastapi_app.routers import post_router, auth_router

# 🔹 Nạp môi trường Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

app = FastAPI()

# 🔹 Gắn router
app.include_router(auth_router.router)
app.include_router(post_router.router)





