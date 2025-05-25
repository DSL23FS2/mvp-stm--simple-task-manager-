def model_to_dict_list(models: list) -> list[dict]:
    """
    Преобразует список объектов SQLAlchemy в список словарей.
    Удаляет служебное поле `_sa_instance_state`.

    :param models: Список объектов SQLAlchemy.
    :return: Список словарей.
    """
    result = []
    for model in models:
        model_dict = model.__dict__.copy()  # Создаем копию словаря объекта
        model_dict.pop('_sa_instance_state', None)  # Удаляем служебное поле
        result.append(model_dict)
    return result