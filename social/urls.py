from django.urls import path
from . import views

urlpatterns = [
    path('', views.share, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('like', views.like, name="like"),
    path('post/<int:id>', views.singlePost, name="post"),
    path('add_comment/<int:id>', views.comment, name="comment"),
    path('like_comment', views.like_comment, name="like_comment"),
    path('delete_post/<int:id>', views.delete_post, name="delete_post"),
    path('delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    path('edit', views.edit, name="edit"),
    path('edit_comment', views.edit_comment, name="edit_comment")
]