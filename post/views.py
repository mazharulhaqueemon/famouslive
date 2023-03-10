from django.shortcuts import render
from .models import post,Like,Comment,PostImage,PostVideo
from .serializer import CommentSerializer,ImageSerializer,VideoSerializer,postsreializer,LikeSerializer
from rest_framework import generics


class Postcreatapi(generics.CreateAPIView):
    queryset = post.objects.all()
    serializer_class = postsreializer

class Postretriveapi(generics.RetrieveUpdateDestroyAPIView):
    queryset = post.objects.all()
    serializer_class = postsreializer

class PostCommentCreateapi(generics.ListCreateAPIView):
    queryset = post.objects.all()
    serializer_class = CommentSerializer

class PostLikeCreateapi(generics.ListCreateAPIView):
    queryset = post.objects.all()
    serializer_class = LikeSerializer





# Create your views here.
