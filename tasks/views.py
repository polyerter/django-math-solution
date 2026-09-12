from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TaskType, Calculation
from django.http import JsonResponse
import json

from .services.computations import factory



# @login_required
def task_list(request):
    """список задач"""

    tasks = TaskType.objects.filter(is_active=True)

    return render(request, 'tasks/list.html', {'tasks': tasks})
    # return JsonResponse({'tasks':"data"})
    
def task_detail(request,  slug=None):
    task = TaskType.objects.filter(is_active=True, slug=slug).get()

    # request_data = request.POST

    # print(task.input_schema)

    # computation = factory.get(slug)

    # print(request_data)

    return render(request, 'tasks/detail.html', {'task_type': task})