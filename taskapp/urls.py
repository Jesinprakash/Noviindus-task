from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from taskapp.views import UserTaskListView, TaskUpdateView, TaskReportView,CreateUserView,UserLogin,TaskCreateView,TaskDeleteView




urlpatterns = [
    path('tasks/', UserTaskListView.as_view()),
    path('tasks/<int:pk>/', TaskUpdateView.as_view()),
    path('tasks/<int:pk>/report/', TaskReportView.as_view()),
    path('register/',CreateUserView.as_view()),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('task/destroye/<int:pk>/',TaskDeleteView.as_view()),
    path('task/login/',UserLogin.as_view()),
    path('task/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    


    
]

