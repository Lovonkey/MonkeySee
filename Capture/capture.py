import cv2
import subprocess
import os
import time
import psutil

class win_camera(object):
	def __init__(self):
		self.path_to_watch = "C:\\Users\\Lovon\\Pictures\\Camera Roll"
		self.before = dict([(f, None) for f in os.listdir (self.path_to_watch)])
		subprocess.Popen("start microsoft.windows.camera:", shell=True)

	def capture(self):
		fs = []
		after = dict ([(f, None) for f in os.listdir (self.path_to_watch)])
		added = [f for f in after if not f in self.before]
		if added:
			self.before = after
			for i in added:
				fs.append(os.path.join(self.path_to_watch, i))
			return (";".join(fs), self.path_to_watch)
		else:
			return ("",self.path_to_watch)
	
	def is_running(self):
		for i in  psutil.pids():
			try:
				p = psutil.Process(i)
				if p.name() == "WindowsCamera.exe":
					return True
			except:
				continue
		return False

	def close(self):
		for i in  psutil.pids():
			try:
				p = psutil.Process(i)
				if p.name() == "WindowsCamera.exe":
					p.kill()
					break
			except:
				continue

if __name__ == '__main__':
    ws = win_camera()
    while True:
        time.sleep(5)
        print(ws.capture())