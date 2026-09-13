from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import TaskType, Calculation

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
        try:
            computation = factory.get(slug)

            form_data = request.POST
            
            if not computation:
                raise ValueError(f"Калькулятор с {slug} не найден")
            computation = computation()
    
            inputs: dict[str, InputSchema] = parse_form(task_type, form_data)
    
            calculation = Calculation(
                user=request.user,
                inputs={k:x.value for k, x in inputs.items()},
                task_type=task_type,
            )
    
            output  = computation.solve(**calculation.inputs)

            result = output
    
            calculation.results = output
            calculation.is_success = True
            calculation.save()

            messages.success(request, "Вычисление выполнено успешно!")
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Ошибка вычисления: {e}")

    return render(request, 'tasks/detail.html', {
        'task_type': task_type,
        'result': result,
        # 'plot_url': plot_url,
        'form_data': form_data,
    })

