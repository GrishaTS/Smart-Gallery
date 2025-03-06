import flet as ft

class AppBarMixin:
    APP_BAR_TITLE_ROUTE: str = None
    APP_BAR_THEME: bool = True
    APP_BAR_CONFIRM_DELETION: bool = False
    APP_BAR_DELETE_ALL: bool = False
    APP_BAR_SORTING: bool = False
    APP_BAR_UPLOAD: bool = False

    def __init__(self):
        self.title = None
        self.actions = []
        super().__init__()
        self.page: ft.Page
    
    def app_bar(self):
        self.add_title()
        if self.APP_BAR_CONFIRM_DELETION:
            self.add_confirm_deletion_button()
        if self.APP_BAR_DELETE_ALL:
            self.add_delete_button()
        if self.APP_BAR_UPLOAD:
            self.add_upload_button()
        if self.APP_BAR_SORTING:
            self.add_sorting_button()
        if self.APP_BAR_THEME:
            self.add_theme_button()
        self.appbar = ft.AppBar(
            title=self.title,
            center_title=False,
            actions=self.actions
        )
    
    def add_title(self):
        if not self.APP_BAR_TITLE_ROUTE:
            span = ft.TextSpan(
                'Smart Gallery',
                style=ft.TextStyle(color=ft.colors.BLUE, weight='w500'),
                url='https://github.com/GrishaTS/Smart-Gallery',
            )
        else:
            span = ft.TextSpan(
                'Smart Gallery',
                style=ft.TextStyle(color=ft.colors.BLUE, weight='w500'),
                on_click=lambda e: self.page.go(self.APP_BAR_TITLE_ROUTE),
            )
        self.title = ft.Text(spans=[span])

    def add_theme_button(self):
        def toggle_theme(e: ft.ControlEvent):
            e.page.theme_mode = 'dark' if e.page.theme_mode == 'light' else 'light'
            e.page.update()
        
        self.actions.append(ft.IconButton(ft.Icons.BRIGHTNESS_4, on_click=toggle_theme, tooltip='Переключить тему'))

    def add_sorting_button(self):
        if not hasattr(self, 'set_sorting'):
            raise AttributeError('set_sorting не инициализирована')
        self.actions.append(ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text='По дате', on_click=lambda e: self.set_sorting('uploaded_at')),
                ft.PopupMenuItem(text='По размеру', on_click=lambda e: self.set_sorting('size')),
            ],
            icon=ft.Icons.SORT,
            tooltip='Отсортировать'
        ))
    
    def add_upload_button(self):
        if not hasattr(self, 'on_files_picked'):
            raise AttributeError('on_files_picked не инициализирована')
        if not hasattr(self, 'on_files_upload'):
            raise AttributeError('on_files_upload не инициализирована')
        self.file_picker = ft.FilePicker(on_result=self.on_files_picked, on_upload=self.on_files_upload)
        self.page.overlay.append(self.file_picker)
        self.actions.append(ft.IconButton(
            ft.icons.UPLOAD_FILE,
            on_click=lambda e: self.file_picker.pick_files(allowed_extensions=['png', 'jpg', 'jpeg'],
                                                      allow_multiple=True),
            tooltip='Добавить',
        ))

    def add_delete_button(self):
        if not hasattr(self, 'delete'):
            raise AttributeError('delete не инициализирована')
        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            on_click=lambda e: self.delete(),
            tooltip='Удалить все'
        )
        self.actions.append(self.delete_button)

    def add_confirm_deletion_button(self):
        if not hasattr(self, 'confirm_deletion'):
            raise AttributeError('confirm_deletion не инициализирована')
        self.confirm_deletion_button = ft.ElevatedButton(
            text='Подтвердить',
            on_click=lambda e: self.confirm_deletion(),
            icon=ft.icons.CHECK,
            bgcolor=ft.colors.RED_200,
            color=ft.colors.WHITE,
            icon_color=ft.colors.WHITE,
            style=ft.ButtonStyle(text_style=ft.TextStyle(
                weight=ft.FontWeight.BOLD,
            )),
            disabled=True
        )
        self.actions.append(self.confirm_deletion_button)


