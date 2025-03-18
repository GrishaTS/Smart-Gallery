from dataclasses import dataclass


@dataclass(frozen=True)
class ViewRoutes:
    """
    Класс для хранения маршрутов приложения.
    """

    HOME: str = "/"
    IMAGE: str = "/image/:image_id"
    IMAGES: str = "/images"
    DELETE_IMAGES: str = "/delete"
    SEARCH_IMAGES: str = "/search"

    @staticmethod
    def build(route: str, **args) -> str:
        """
        Формирует маршрут с подстановкой аргументов.

        :param route: Маршрут с параметрами.
        :param args: Аргументы для подстановки в маршрут.
        :return: Готовый маршрут.
        """
        for key, value in args.items():
            route = route.replace(f":{key}", str(value), 1)
        return route
