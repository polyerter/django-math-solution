from dataclasses import dataclass


@dataclass
class InputSchema:
    name: str
    label: str | None
    placeholder: str | None
    
    type: str | None
    value: str | None
    required: bool = True

    default: str | None = ''
    hint: str | None = None

    # для чисел
    step: float | None = None
    min: float | None = None
    max: float | None = None

    # для list
    min_length: int | None = None
    separator: str = ','

    def __post_init__(self):
        # if not self.value.strip():
        #     return
        
        raw_value = self.value.strip()

        self.value = raw_value

        if self.required and not raw_value:
            raise ValueError(f'Поле «{self.label}» является обязательным')

        field_type = type(self.value)
        try:
            # ============= float =============
            if self.type == 'float':
                self.value = float(self.value.replace(',', '.'))
                self._check_range()
            # ============= int =============
            elif self.type == 'int':
                self.value = int(self.value)
                self._check_range()
            # ============= text =============
            elif self.type == 'text':
                ...
            # ============= textarea =============
            elif self.type == 'textarea':
                ...
            # ============= select =============
            elif self.type == 'select':
                ...
            # ============= list =============
            elif self.type == 'list':
                items = [x.strip() for x in self.value.split(self.separator) if x.strip()]

                if self.min_length and len(items) < self.min_length:
                    raise ValueError(f"Минимум {self.min_length} элементов")

                try:
                    self.value = [float(x.replace(',', '.')) for x in items]
                except:
                    # если не числа
                    return items
            # ============= matrix =============
            elif self.type == 'matrix':
                ...
            else:
                raise ValueError(f"Неизвестный тип поля: {field_type}")

        except ValueError as e:
            if "could not convert" in str(e).lower():
                raise ValueError(f"Поле «{self.label}» - введите корректное число")
            raise

    def _check_range(self):
        if self.min is not None and self.value < self.min:
            raise ValueError(f"Поле «{self.label}»: значение должно быть ≥ {self.min}")

        if  self.max is not None and self.value > self.max:
            raise ValueError(f"Поле «{self.label}»: значение должно быть ≤ {self.max}")
        