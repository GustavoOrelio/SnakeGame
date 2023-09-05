from Object import Object


class SnakeSegment(Object):
    def __init__(self, sprite_input, position, size, direction):
        super().__init__(sprite_input, position, size)
        self.direction = direction  # direção atual deste segmento
        self.prev_direction = direction  # direção anterior deste segmento
