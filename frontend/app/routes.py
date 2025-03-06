from dataclasses import dataclass

@dataclass
class ViewRoutes:
    HOME = '/'
    IMAGE = '/image/:image_id'
    IMAGES = '/images'
    DELETE_IMAGES = '/delete'
    SEARCH_IMAGES = '/search'

    @staticmethod
    def build(route: str, **args):
        for key, value in args.items():
            route = route.replace(f':{key}', str(value), 1)
        return route
