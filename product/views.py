from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, pagination, filters

from rest_framework.response import Response

from rest_framework.decorators import action
from django.db.models import Q


from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAuthorPermission
# Create your views here.

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorPermission)

    # pagination_class = pagination.LimitOffsetPagination
    # search_fields = ('title', 'description')
    # filter_backends = (filters.SearchFilter, )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


    @action(detail=False, methods=['GET'])
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset()
        if query == 'available':
            # available products
            queryset = queryset.filter(available=True)
        elif query:
            # search
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))

        price = request.query_params.get('price')
        if price == 'asc':
            queryset = queryset.order_by('price')
        elif price =='desc':
            queryset = queryset.order_by('-price')

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

