"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter



# --- Thiết lập môi trường Django ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# --- Khởi động Django trước khi import model hoặc routing ---
django.setup()

# **QUAN TRỌNG:** Import file routing của app sẽ chứa WebSocket của bạn
import blog.routing # Ví dụ: Nếu bạn đặt WebSocket trong app 'blog'

print("ASGI application loaded (Channels đang hoạt động)")

# --- Tạo ứng dụng HTTP ---
django_asgi_app = get_asgi_application()

# --- Gộp HTTP + WebSocket ---
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            blog.routing.websocket_urlpatterns
        )
    ),
})
