import pygame

class Text:
    def __init__(self, text, text_object, text_rect_object) -> None:
        self.text = text
        self.text_object = text_object
        self.text_rect_object = text_rect_object
        self.x = 0
        self.y = 0
    
    text: str
    text_object: pygame.Surface
    text_rect_object: any
    x: int
    y: int