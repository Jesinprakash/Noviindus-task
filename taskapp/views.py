from rest_framework import generics, permissions, status,authentication
from rest_framework.response import Response
from taskapp.models import Task,User
from taskapp.serializers import TaskSerializer, TaskUpdateSerializer,UserSerializer
from taskapp.permissions import IsAdminOrSuperAdmin
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied


from rest_framework.exceptions import ValidationError  



class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperAdmin]  

    def perform_create(self, serializer):
        serializer.save()

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save()




class UserTaskListView(generics.ListAPIView):

    serializer_class = TaskSerializer

    permission_classes = [permissions.IsAuthenticated]

    authentication_classes=[JWTAuthentication]

    def get_queryset(self):

        return Task.objects.filter(assigned_to=self.request.user)

class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]  

    # def perform_update(self, serializer):
    #     task = self.get_object()
    #     user = self.request.user

        # Prevent user from updating others' tasks
        # if user.role == "user" and task.assigned_to != user:
        #     raise ValidationError("You are not allowed to update this task.")

        # status = self.request.data.get('status')

        # if status == 'Completed':
        #     completion_report = self.request.data.get('completion_report', '').strip()
        #     worked_hours = self.request.data.get('worked_hours')

        #     if not completion_report or worked_hours is None:
        #         raise ValidationError("Both Completion Report and Worked Hours are required to complete the task.")

        #     try:
        #         worked_hours = float(worked_hours)
        #         if worked_hours < 0:
        #             raise ValidationError("Worked Hours must be a non-negative number.")
        #     except ValueError:
        #         raise ValidationError("Worked Hours must be a number.")

        # serializer.save()

    def get_object(self):
            task = super().get_object()

            # Only the assigned user can update the task
            if task.assigned_to != self.request.user:
                raise PermissionDenied("You can only update tasks assigned to you.")

            return task


class TaskReportView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]
    authentication_classes=[JWTAuthentication]
    queryset = Task.objects.filter(status='Completed')

class TaskDeleteView(generics.DestroyAPIView):

    serializer_class=TaskSerializer

    queryset=Task.objects.all()

    permission_classes=[IsAdminOrSuperAdmin]

    authentication_classes=[JWTAuthentication]



class UserLogin(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def post(self, request, *args, **kwargs):

        username = request.data.get("username")

        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
           
            refresh = RefreshToken.for_user(user)

            access_token = refresh.access_token

            return Response({
                'refresh': str(refresh),
                'access': str(access_token)
            })

        return Response({"error": "Invalid credentials"})
