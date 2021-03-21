from django.contrib import admin
from django.urls import path
from . import views

from account.views import (comment_home, comment_create, comment_update, comment_delete)



urlpatterns = [
  path('<pk>/clist', comment_home, name='comments'),
  path('new/', comment_create, name='new-comment'),
  path('<pk>/update/', comment_update, name='update-comment'),
  path('<pk>/delete/', comment_delete, name='delete-comment'),
]
