from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.postView, name='register'),
    path('login/', views.getView, name='login'),
    path('todo/', views.todoView, name='todo'),  # POST to create a todo
    path('todo/<int:id>/', views.update_task, name='update-task'),  # PATCH to update a todo
    path('todo/delete/<int:id>/', views.delete_task, name='delete-task'),  # DELETE to delete a todo
]
