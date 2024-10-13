import pygame_menu

class Menu(pygame_menu.Menu):
    def __init__(self, title: str, width: int, height: int, theme=None, options={}, position=(0, 0, False)):
        super().__init__(title, width, height, theme=theme if theme else self.getMainTheme(), position=position)
        self.setTitle(title)
        self.setOptions(options)
        
    def setTitle(self, title: str):
        """
        Set title for the menu.

        Args:
            title (str): The title to display.
        """
        label = self.add.label(
            title,
            float=True,
            font_size=46,
            font_name=pygame_menu.font.FONT_8BIT,
            margin=(0, 8),
        )
        label.translate(0, -120)
    
    def setOptions(self, options: dict):
        """
        Configure the menu options such as buttons and inputs.
        """
        if 'inputs' in options:
            self._add_inputs(options['inputs'])
        
        if 'buttons' in options:
            self._add_buttons(options['buttons'])
            
    def _add_inputs(self, inputs: dict):
        """
        Add text inputs to the menu.

        Args:
            inputs (dict): A dictionary of input labels and default values.
        """
        for label, value in inputs.items():
            self.add.text_input(
                f'{label}: ', 
                default=value, 
                font_name=pygame_menu.font.FONT_NEVIS, 
                font_size=26, 
                margin=(0, 8), 
                padding=10
            )

    def _add_buttons(self, buttons: dict):
        """
        Add buttons to the menu.

        Args:
            buttons (dict): A dictionary of button labels and actions.
        """
        for label, action in buttons.items():
            self.add.button(
                label, 
                action, 
                font_name=pygame_menu.font.FONT_8BIT, 
                font_size=26, 
                margin=(0, 8), 
                padding=10
            )

    def getMainTheme(self):
        """
        Get the default theme for the menu.

        Returns:
            main_theme (pygame_menu.Theme): The main theme with customized settings.
        """
        BACKGROUND = (34, 40, 44)
        main_theme = pygame_menu.themes.THEME_DARK.copy()
        main_theme.title = False
        main_theme.background_color = BACKGROUND
        return main_theme
    