from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import viewsets, status

from .permissions import IsOwnerOrReadOnly
from .models import Category, Note
from .serializers import CategorySerializer, NoteSerializer


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


class NoteView(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    # when a category is posted grab the user id who made the request to use it later on as a foreign key
    def perform_create(self, serializer):
        _category_id = self.request.data['category']
        _category = Category.objects.filter(id=_category_id).first()
        if _category.user == self.request.user:
            serializer.save(user=self.request.user)

    # return only the user's categories
    def get_queryset(self):
        return Note.objects.filter(category__user=self.request.user)
