from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users import views


router = SimpleRouter()
router.register(r'auth',
                views.RegistrationModelViewSet)


urlpatterns = [
    path('', include(router.urls))
]

