from django.urls import path, include
from rest_framework.routers import SimpleRouter

from innotwits import views


router = SimpleRouter()
router.register(r'page',
                views.PageViewSet)

router.register(r'post',
                views.PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]
