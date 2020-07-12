import cv2

class app(object):
	def __init__(self):
		self.cap = None
		for i in range(3,-1,-1):
			cap = cv2.VideoCapture(i)
			if cap.isOpened():
				cap.set(3, 1920)
				cap.set(4, 1080)
				self.cap = cap
				break

	def isOpened(self):
		if self.cap is None:
			return False
		else:
			return True
	
	def capture(self):
		if self.isOpened():
			ret, frame = self.cap.read()
			data = cv2.resize(frame, (960, 540))
			return cv2.imencode('.png', data)[1].tobytes()
		return None
	
	def close(self):
		self.cap.release()
		cv2.destroyAllWindows()