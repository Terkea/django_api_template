from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('category', views.CategoryView)
router.register('note', views.NoteView)

urlpatterns = [
    path('', include(router.urls)),
]