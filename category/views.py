from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import viewsets

from .models import Category
from .permissions import IsOwnerOrReadOnly
from .serializers import CategorySerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    # when a category is posted grab the user id who made the request to use it later on as a foreign key
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # return only the user's categories
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).all()