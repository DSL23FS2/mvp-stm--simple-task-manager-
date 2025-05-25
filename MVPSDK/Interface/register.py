from sqlalchemy import Table, Column
from sqlalchemy.orm import registry

class Register:
    @staticmethod
    def map_model_to_base(model_class, base):
        """
        Привязывает модель к метаданным Base с использованием registry.
        :param model_class: Класс модели (без контекста).
        :param base: Объект Base (declarative_base).
        """
        # Фильтруем атрибуты модели, чтобы выбрать только колонки
        columns = []
        for attr_name, attr_value in vars(model_class).items():
            if isinstance(attr_value, Column):
                # Если у колонки нет имени, задаём его как имя атрибута
                if not attr_value.name:
                    attr_value.name = attr_name
                columns.append(attr_value)

        # Проверяем, есть ли хотя бы одна колонка с primary_key=True
        if not any(col.primary_key for col in columns):
            raise ValueError(f"Model {model_class.__name__} must have at least one primary key column.")

        # Создаём таблицу
        table = Table(
            model_class.__tablename__,
            base.metadata,
            *columns
        )

        # Привязываем модель к таблице
        base.registry.map_imperatively(model_class, table)