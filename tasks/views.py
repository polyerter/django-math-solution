from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TaskType, Calculation
from django.http import JsonResponse

from .application.services.computations import factory
from .application.services.parser import parse_form
from .application.domain.input_schema import InputSchema


# @login_required
def task_list(request):
    """список задач"""

    tasks = TaskType.objects.filter(is_active=True)

    return render(request, 'tasks/list.html', {'tasks': tasks})
    # return JsonResponse({'tasks':"data"})
    
def task_detail(request,  slug=None):
    task_type = get_object_or_404(TaskType, slug=slug, is_active=True)

    if request.method == 'POST':
        computation = factory.get(slug)

        if not computation:
            raise ValueError(f"Калькулятор с {slug} не найден")

        inputs: dict[str, InputSchema] = parse_form(task_type, request.POST)

        print(inputs)
        # print(task.input_schema)
        # print(request_data)


        print('task_detail')

        # return
    # else:
    return render(request, 'tasks/detail.html', {'task_type': task_type})

