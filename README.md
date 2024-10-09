# Introdution
This game is built on python language, can be played on computer, play LAN.
# Library
    * `TextInputVisualizer` which can be used to both manage and draw text input. Simply pass all events returned by `pygame.event.get()` to it every frame, and blit its `surface` attribute on the screen.
    *  `TextInputManager` that can be used to just manage inputted text, with no visual aspect. Used by `TextInputVisualizer` behind the scenes.