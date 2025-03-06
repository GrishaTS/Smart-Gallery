import flet as ft

class NavBarMixin:
    NAV_BAR_POS: int
    NAV_BAR_ICON: ft.Icons
    NAV_BAR_LABEL: str

    def __init__(self):
        super().__init__()
        self.page: ft.Page

    def add_nav_bar(self) -> None:
        self.nav_bar_classes: list[NavBarMixin] = sorted(
            NavBarMixin.__subclasses__(),
            key=lambda cls: cls.NAV_BAR_POS
        )
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=cls.NAV_BAR_ICON, label=cls.NAV_BAR_LABEL, tooltip='')
                for cls in self.nav_bar_classes
            ],
            selected_index=self.nav_bar_classes.index(self.__class__),
            on_change=self.on_nav_change,
        )

    def on_nav_change(self, e: ft.ControlEvent) -> None:
        selected_class: NavBarMixin = self.nav_bar_classes[e.control.selected_index]
        self.page.go(selected_class.ROUTE)
