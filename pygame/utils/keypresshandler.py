import pygame

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d, K_k, K_j, K_h, K_l, K_RETURN

from .controllerhandler import ControllerHandler
J_UP = ControllerHandler.J_UP
J_DOWN = ControllerHandler.J_DOWN
J_RIGHT = ControllerHandler.J_RIGHT
J_LEFT = ControllerHandler.J_LEFT

class KeyPressHandler:
    lastPressed = set()

    @classmethod
    def update(cls, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                cls.lastPressed.add(event.key)
            elif event.type == pygame.KEYUP:
                cls.lastPressed.remove(event.key)
            elif event.type == pygame.JOYAXISMOTION and ControllerHandler.active():

                for key in ControllerHandler.getKeys():
                    if key in cls.lastPressed:
                        cls.lastPressed.remove(key)
                cls.lastPressed.update(ControllerHandler.getPressed())


    @classmethod
    def pressed(cls, keys, single=False):
        single = bool(single)
        if not isinstance(keys, list):
            keys = [keys]
        pressed_keys = pygame.key.get_pressed()
        controller_pressed_keys = ControllerHandler.getPressed()

        if single:
            return any((pressed_keys[key] or key in controller_pressed_keys) and key not in cls.lastPressed for key in keys)
        return any((pressed_keys[key] or key in controller_pressed_keys) for key in keys)

    # Helpers
    @classmethod
    def enter(cls, single=True):
        return cls.pressed(K_RETURN, single=single)

    @classmethod
    def up(cls, single=True):
        keys = [K_UP, K_w, K_k, J_UP]
        return cls.pressed(keys, single=single)

    @classmethod
    def down(cls, single=True):
        keys = [K_DOWN, K_s, K_j, J_DOWN]
        return cls.pressed(keys, single=single)

    @classmethod
    def right(cls, single=True):
        keys = [K_RIGHT, K_d, K_l, J_RIGHT]
        return cls.pressed(keys, single=single)

    @classmethod
    def left(cls, single=True):
        keys = [K_LEFT, K_a, K_h, J_LEFT]
        return cls.pressed(keys, single=single)


