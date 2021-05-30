
import pygame

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d, K_k, K_j, K_h, K_l, K_RETURN

class KeyPressHandler:
    lastPressed = list()

    @classmethod
    def update(cls, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                cls.lastPressed.append(event.key)
            elif event.type == pygame.KEYUP:
                cls.lastPressed.remove(event.key)

    @classmethod
    def pressed(cls, keys, single=False):
        single = bool(single)
        if not isinstance(keys, list):
            keys = [keys]
        pressed_keys = pygame.key.get_pressed()
        if single:
            return any(pressed_keys[key] and key not in cls.lastPressed for key in keys)
        return any(pressed_keys[key] for key in keys)

    # Helpers
    @classmethod
    def enter(cls, single=True):
        return cls.pressed(K_RETURN, single=single)

    @classmethod
    def up(cls, single=True):
        keys = [K_UP, K_w, K_k]
        return cls.pressed(keys, single=single)

    @classmethod
    def down(cls, single=True):
        keys = [K_DOWN, K_s, K_j]
        return cls.pressed(keys, single=single)

    @classmethod
    def right(cls, single=True):
        keys = [K_RIGHT, K_d, K_l]
        return cls.pressed(keys, single=single)

    @classmethod
    def left(cls, single=True):
        keys = [K_LEFT, K_a, K_h]
        return cls.pressed(keys, single=single)


