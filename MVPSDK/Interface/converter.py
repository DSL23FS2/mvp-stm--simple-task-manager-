from typing import Type, TypeVar, Any
from dataclasses import fields
from sqlalchemy.orm.attributes import InstrumentedAttribute

TDataclass = TypeVar("TDataclass")  # Тип для dataclass
TORMModel = TypeVar("TORMModel")    # Тип для ORM-модели

class Converter:
    @staticmethod
    def model_to_dataclass(
        model_obj: TORMModel, 
        dataclass_type: Type[TDataclass]
        ) -> TDataclass:
        """
        Конвертирует ORM-модель в dataclass.
        :param model: Экземпляр ORM-модели.
        :param dataclass_type: Класс dataclass, в который нужно конвертировать.
        :return: Экземпляр dataclass.
        """
        dataclass = {
            field.name: getattr(model_obj, field.name) 
            for field in fields(dataclass_type)
            }
        
        return dataclass_type(**dataclass)

    @staticmethod
    def dataclass_to_model(
        dataclass_obj: TDataclass, 
        model_type: Type[TORMModel], 
        exclude_fields: list[str] = None,
        include_id: bool = False
        ) -> TORMModel:
        
        """
        Конвертирует dataclass в ORM-модель.
        :param dataclass_obj: Экземпляр dataclass.
        :param model_type: Класс ORM-модели, в который нужно конвертировать.
        :param exclude_fields: Список полей, которые нужно исключить (например, id).
        :return: Экземпляр ORM-модели.
        """
        
        exclude_fields = exclude_fields or []
        
        # Если id не нужно включать, добавляем его в список исключений
        if not include_id and "id" not in exclude_fields:
            exclude_fields.append("id")
        
        model_data = {
            field_name: getattr(dataclass_obj, field_name) 
            for field_name, field_value in vars(model_type).items()
            if isinstance(field_value, InstrumentedAttribute)
                and field_name not in exclude_fields
            }
        return model_type(**model_data)