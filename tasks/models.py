from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    desctioption = models.TextField(blank=True)

    input_schema = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'math_task_types'


class Calculation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='calculations',
    )

    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.PROTECT,
        related_name='calculations'
    )

    inputs = models.JSONField(default=dict)
    results = models.JSONField(default=dict)

    is_success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    plot = models.ImageField(
        upload_to='plot/%Y/%m',
        null=True,
        blank=True,
    )

    computation_time = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'math_calculations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.task_type.name} - {self.user.username} ({self.created_at:%d/%m/%Y})"