class WebColours():
	def __init__(self):
		self.BLACK = (0, 0, 0)
		self.WHITE = (255, 255, 255)
		self.RED = (255, 0, 0)
		self.YELLOW = (255, 255, 0)
		self.GREEN = (0, 255, 0)
		self.CYAN = (0, 255, 255)
		self.BLUE = (0, 0, 255)
		self.MAGENTA = (255, 0, 255)
		self.BG = (51, 36, 63)
		self.SPACE = (50, 34, 61)

class Settings():
	def __init__(self):
		wc = WebColours()
		self.WIDTH = 1400
		self.HEIGHT = 800
		self.BG = wc.BG
		self.SPACE = wc.SPACE
		self.FPS = 60