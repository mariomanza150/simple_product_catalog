from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import Product, User, UserTypes
from .serializers import ProductSerializer, UserSerializer


# worth looking into django-rest-framework-roles if more complexity required
class IsAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if hasattr(request.user, "user_type") and request.user.user_type != UserTypes.ADMIN:
            return request.method in SAFE_METHODS
        return super().has_permission(request, view)


class UserViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ProductViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.all()
    lookup_field = "sku"

    def get_queryset(self, *args, **kwargs):
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        self.get_object().count_view()
        return super().retrieve(request, *args, **kwargs)
