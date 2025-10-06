from fastapi import APIRouter
from blog.models import Post  # dùng model Django
from django.forms.models import model_to_dict

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
def get_all_posts():
    posts = Post.objects.all().order_by("-id")
    return [model_to_dict(post) for post in posts]