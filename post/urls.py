from django.urls import path
from .views import Postcreatapi,Postretriveapi,PostLikeCreateapi,PostCommentCreateapi

urlpatterns = [
    path('post-create/', Postcreatapi.as_view()),
    path('post-retrieve/<int:pk>/', Postretriveapi.as_view(), name='post-detail'),
    path('post-delete/', Postretriveapi.as_view(), name='like-list'),
    path('like-create/', PostLikeCreateapi.as_view(), name='like-detail'),
    path('comment-create/', PostCommentCreateapi.as_view(), name='comment-list'),
]