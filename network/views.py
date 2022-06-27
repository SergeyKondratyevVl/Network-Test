from django.http import Http404
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.contrib.auth import logout, login
from django.views.generic import CreateView

from .permissions import IsAuthorOrReadOnly, IsNotAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import *
from .serializers import *
from .forms import *

class PostAPIListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000

class PostAPIList(generics.ListCreateAPIView):
    pagination_class = PostAPIListPagination
    queryset = PostNet.objects.all()
    serializer_class = PostNetDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('author', )

# class PostAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PostNet.objects.all()
#     serializer_class = PostNetSerializer
#     permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)

class UserNetListView(generics.ListAPIView):
    queryset = UserNet.objects.all()
    serializer_class = UserNetListSerializer
    permission_classes = (permissions.IsAuthenticated,)

# надо настроить чтобы видели только себя
# class UserNetDetailView(generics.RetrieveAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserNetDetailSerializer
#     queryset = UserNet.objects.all()

class UserNetDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, pk):
        filters = {}
        filters['user'] = UserNet.objects.get(id=pk)
        try:
            filters['posts'], created = PostNet.objects.get_or_create(
            author_id=pk
            )
            serializer = FilterOneSerializers(filters)
            return Response(serializer.data)
        except MultipleObjectsReturned:
            filters['posts'] = PostNet.objects.filter(author_id=pk)
            serializer = FilterManysSerializers(filters)
            return Response(serializer.data)

class PostNetListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostNetDetailSerializer
    pagination_class = PostAPIListPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('author', )

    def get_queryset(self):
        posts = PostNet.objects.all()
        return posts
# class PostNetListView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     pagination_class = PostAPIListPagination
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_fields = ('author', )
#     def get(self, request):
#         filter = {}
#         filter['post'] = PostNet.objects.all()
#         try:
#             filter['images'] = PostImages.objects.all()
#             serializer = PostUpdateOneSerializer(filter)
#             return serializer.data
#         except MultipleObjectsReturned:
#             filter['images'] = PostImages.objects.all()
#             serializer = PostUpdateManySerializer(filter)
#             return serializer.data

class PostCreateAPIView(generics.CreateAPIView):
    queryset = PostNet.objects.all()
    serializer_class = PostNetDetailSerializer
    permission_classes = (permissions.IsAuthenticated, ) #IsAuthorOrReadOnly

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

class PostNetRetrieveAPIView(generics.RetrieveAPIView):
    queryset = PostNet.objects.all()
    serializer_class = PostNetDetailSerializer
    permission_classes = (permissions.IsAuthenticated, )

class PostNetUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostNet.objects.all()
    serializer_class = PostNetUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

class PostImagesListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, pk):
        filters = {}
        filters['post'] = PostNet.objects.get(id=pk)
        try:
            filters['images'], created = PostImages.objects.get_or_create(
            post_id=pk
            )
            serializer = PostUpdateOneSerializer(filters)
            return Response(serializer.data)
        except MultipleObjectsReturned:
            filters['images'] = PostImages.objects.filter(post_id=pk)
            serializer = PostUpdateManySerializer(filters)
            return Response(serializer.data)
    

class PostNetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostNet.objects.all()
    serializer_class = PostNetDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)
    
#    def get_queryset(self):
#        pk = self.kwargs.get('pk')
#        filters = {}
#        filters['post'] = PostNet.objects.get(id=pk)
#        try:
#            filters['images'], created = PostImages.objects.get_or_create(
#            post__id=pk
#            )
#            serializer = PostUpdateOneSerializer(filters)
#            # return Response(serializer.data)
#        except MultipleObjectsReturned:
#            filters['images'] = PostImages.objects.filter(post__id=pk)
#            serializer = PostUpdateManySerializer(filters)
#        return serializer.data

# class PostNetDetailView(APIView):

#     def get_object(self, pk):
#         try:
#             return PostNet.objects.get(pk=pk)
#         except PostNet.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         snippets = PostNet.objects.all()
#         serializer = PostNetDetailSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         filters = {}
#         filters['post'] = PostNet.objects.get(id=pk)
#         try:
#             filters['images'], created = PostImages.objects.get_or_create(
#             post__id=pk
#             )
#             serializer = PostUpdateOneSerializer(filters)
#             # return Response(serializer.data)
#         except MultipleObjectsReturned:
#             filters['images'] = PostImages.objects.filter(post__id=pk)
#             serializer = PostUpdateManySerializer(filters)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     def put(self):
#         pk = self.kwargs.get('pk')
#         filters = {}
#         filters['user'] = PostNet.objects.get(id=pk)
#         try:
#             filters['images'], created = PostImages.objects.get_or_create(
#             post_id=pk
#             )
#             serializer = PostUpdateOneSerializer(filters)
#             return serializer.data
#         except MultipleObjectsReturned:
#             filters['images'] = PostImages.objects.filter(post_id=pk)
#             serializer = PostUpdateManySerializer(filters)
#             return serializer.data

class UserCreateAPIView(generics.CreateAPIView):
    queryset = UserNet.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (IsNotAuthenticated,)

# class PostImagesListAPIView(generics.CreateAPIView):
#     queryset = PostImages.objects.all()
#     serializer_class = ImageDetailSerializer
#     permission_classes = (IsNotAuthenticated, ) #IsAuthorOrReadOnly
#     def get_queryset(self):
#         post = PostImages.objects.get(post=self.pk)
#         return post
    
#     def perform_create(self, serializer):
#         serializer.save(post=self.request)
        
#     def perform_update(self, serializer):
#         serializer.save(post=self.request)

# class PostImagesListAPIView(APIView):  
#     def post(self, request, pk):
#         form = ImageDetailSerializer(request.POST)
#         post = PostNet.objects.get(id=pk)
#         if form.is_valid():
#             form = form.save(commit=False)
#             if request.POST.get("parent", None):
#                 form.parent_id = int(request.POST.get("parent"))
#             form.post = post
#             form.save()
#         print(request.POST)
#         return Response(form.data)
