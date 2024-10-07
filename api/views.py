from django.shortcuts import render
from .serializers import UserSerializer
from .models import RegisterUser,Tasks
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password

# Create your views here.

@api_view(['POST'])
def postView(request):
    """
    Handles user registration by creating a new user with a hashed password.
    """
    if request.method == 'POST':
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate input
        if not all([first_name, last_name, email, password]):
            return Response(
                {'error': 'All fields are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already exists
        if RegisterUser.objects.filter(email=email).exists():
            return Response(
                {'error': 'User with this email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create and save the new user with hashed password
        user = RegisterUser(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)  # This hashes and saves the password

        return Response(
            {'message': 'User registered successfully.'},
            status=status.HTTP_201_CREATED
        )





@api_view(['POST'])
def getView(request):
    """
    Handles user login by verifying email and password.
    """
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate input
        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user exists in the database
        try:
            user = RegisterUser.objects.get(email=email)
        except RegisterUser.DoesNotExist:
            return Response(
                {'error': 'User does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify the password using the model's check_password method
        if user.check_password(password):
            return Response(
                {'message': 'Login successful.','first_name':user.first_name,'last_name':user.last_name},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid password.'},
                status=status.HTTP_400_BAD_REQUEST
            )


#below view for the handle  todo
@api_view(['GET', 'POST'])
def todoView(request):
    if request.method == 'GET':
        tasks = Tasks.objects.all()
        task_list = [{'id': task.id, 'todo': task.todo, 'completed': task.completed} for task in tasks]
        return Response(task_list)  # Return list of todos

    elif request.method == 'POST':
        todo_text = request.data.get('todo')
        todo_item = Tasks(todo=todo_text, completed=False)  # Assuming new tasks start as not completed
        todo_item.save()

        # Return success message along with the created task
        return Response({
            'message': 'Todo added successfully',
            'tasks': {
                'id': todo_item.id,
                'todo': todo_item.todo,
                'completed': todo_item.completed
            }
        }, status=201)




@api_view(['PATCH'])
def update_task(request, id):
    try:
        # Get the task to be updated
        task = Tasks.objects.get(id=id)
    except Tasks.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get the 'completed' status from the request body
    completed = request.data.get('completed', None)
    
    if completed is not None:
        # Update the completed status and save the task
        task.completed = completed
        task.save()

        return Response({'message': 'Task updated successfully', 'task': {'id': task.id, 'todo': task.todo, 'completed': task.completed}}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['DELETE'])
def delete_task(request, id):
    try:
        # Get the task to be deleted
        task = Tasks.objects.get(id=id)
    except Tasks.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Delete the task
    task.delete()

    return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
