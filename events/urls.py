from django.urls import path, include
from rest_framework import routers

from events import views


router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('register', views.CreateUserView.as_view())
]
