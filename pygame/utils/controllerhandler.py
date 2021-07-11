import pygame

class ControllerHandler:
	'''
		Based of the retrolink nes controller
	'''

	# Custom joystick keys
	J_UP = 1337
	J_DOWN = 1338
	J_RIGHT = 1339
	J_LEFT = 1340

	J_A = 1341
	J_B = 1342
	J_SELECT = 1343
	J_START = 1344

	joystick = None

	@classmethod
	def init(cls):
		if not pygame.joystick.get_init():
			pygame.joystick.init()
		try:
			cls.joystick = pygame.joystick.Joystick(0)
			cls.joystick.init()
		except:
			print('Failed to initialize joystick')
			cls.joystick = None

	@classmethod
	def active(cls):
		return pygame.joystick.get_init() and bool(cls.joystick)

	@classmethod
	def getEvents(cls):
		return [pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]

	@classmethod
	def getKeys(cls):
		return [cls.J_UP, cls.J_DOWN, cls.J_RIGHT, cls.J_LEFT, cls.J_A, cls.J_B, cls.J_SELECT, cls.J_START]

	@classmethod
	def getPressed(cls):
		x = [
			(cls.up, cls.J_UP),
			(cls.down, cls.J_DOWN),
			(cls.right, cls.J_RIGHT),
			(cls.left, cls.J_LEFT),
			(cls.a, cls.J_A),
			(cls.b, cls.J_B),
			(cls.select, cls.J_SELECT),
			(cls.start, cls.J_START)
		]
		return [key for f, key in x if f()]

	@classmethod
	def up(cls):
		if not cls.active(): return False
		return bool(cls.joystick.get_axis(1) <= -0.5)

	@classmethod
	def down(cls):
		if not cls.active(): return False
		return bool(cls.joystick.get_axis(1) >= 0.5)

	@classmethod
	def right(cls):
		if not cls.active(): return False
		return bool(cls.joystick.get_axis(0) >= 0.5)

	@classmethod
	def left(cls):
		if not cls.active(): return False
		return bool(cls.joystick.get_axis(0) <= -0.5)

	@classmethod
	def a(cls):
		if not cls.active(): return False
		return bool(cls.joystick.get_button(1))

	@classmethod
	def b(cls):
		if not cls.active(): return False
		return bool(cls.joystick.get_button(2))

	@classmethod
	def select(cls):
		if not cls.active(): return False
		return bool(cls.joystick.get_button(8))

	@classmethod
	def start(cls):
		if not cls.active(): return False
		return bool(cls.joystick.get_button(9))
