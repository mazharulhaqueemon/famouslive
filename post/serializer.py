from rest_framework import serializers
from .models import post, Like, PostVideo, PostImage, Comment



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'profile', 'text', 'created_at')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'post', 'profile', 'created_at')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        likes = LikeSerializer(many=True, read_only=True)
        fields =  ('id', 'image','likes')

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = '__all__'



class postsreializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True,required=False)
    video = VideoSerializer(many=True, read_only=True,required=False)
    class Meta:
        model =post
        fields = '__all__'
        # fields = ('id', 'text', 'profile', 'created_at', 'comments', 'updated_datetime', 'images', 'video', 'likes')