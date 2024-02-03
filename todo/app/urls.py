from django.urls import path
from .views import (TaskView, TaskDetail, TaskCreate, TaskUpdate, 
                    TaskDelete, CustomLoginView, RegisterPage)
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
    path("register/", RegisterPage.as_view(), name="register"),

    path("", TaskView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetail.as_view(), name="task-detail"),
    path("tasks-update/<int:pk>/", TaskUpdate.as_view(), name="task-update"),
    path("tasks-delete/<int:pk>/", TaskDelete.as_view(), name="task-delete"),
    path("create-task/", TaskCreate.as_view(), name="task-create"),
]
