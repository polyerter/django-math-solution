from typing import Any
from tasks.application.domain.input_schema import InputSchema

def parse_form(task_type, post_data: dict) -> dict[str, InputSchema]:
    """
    Парсит всю форму целиком по схеме task_type.input_schema.
    
    Returns:
        dict: {field_name: parsed_value}
    
    Raises:
        ValueError: с описанием первой ошибки
    """

    if not task_type.input_schema:
        return ValueError(f'Схема для модели {task_type} не найдена')

    inputs = {}
    errors = []

    for field in task_type.input_schema:
        name = field['name']
        raw = post_data.get(name, '')

        try:
            inputs[name] = InputSchema(**field, value=raw)
        except Exception as e:
            errors.append(str(e))

    if errors:
        raise ValueError("; ".join(errors))

    return inputs



