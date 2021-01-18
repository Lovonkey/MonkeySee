from DuniangOCR import ocr
from Capture import capture
from File import f
import PySimpleGUI as sg
import cv2
import time
import os
import urllib

ConfigKeys = os.path.join(os.getcwd(), "Conf", "key.txt")

def image_windows_show(outdir=""):
	image = [
		[sg.Text('选择你要读取的发票')],
		[sg.Input(key='_FILES_'),sg.FilesBrowse(file_types=(("image", "*.png *.jpg *.pdf"),))],
		[sg.Text(('选择文件输出路径(默认路径:%s)' % outdir))],
		[sg.Input(key='_DIR_', default_text=outdir),sg.FolderBrowse()],
		[sg.OK()]
	]
	form = sg.FlexForm('猴子选图')
	form.Layout(image)
	button_name,values = form.Read()
	form.close()
	return (values["_FILES_"],values["_DIR_"])

class MainWindow(object):
	def __init__(self):
		ocr = [
				[sg.Text("-" * 90)],
				[sg.Text("BaiDu OCR")],
				[sg.Text("API_KEY:", size=(12,1)), sg.Input(size=(30,1), key='API_KEY', default_text="", font='Song 10')],
				[sg.Text("SECRET_KEY:", size=(12,1)), sg.Input(size=(30,1), key='SECRET_KEY', default_text="", font='Song 10')]
			]

		inv = [
				[sg.Text("-" * 90)],
				[sg.Text("发票信息选择")],
				[sg.Checkbox("收票公司", size=(7,1)), 	sg.Checkbox("发票日期", size=(7,1)), sg.Checkbox("发票号码", size=(7,1)),sg.Checkbox("发票代码", size=(7,1))],
				[sg.Checkbox("单位名称", size=(7,1)),	sg.Checkbox("货物名称", size=(7,1)), sg.Checkbox("规格型号", size=(7,1)), sg.Checkbox("单位", size=(7,1))],
				[sg.Checkbox("数量", size=(7,1)),		sg.Checkbox("单价", size=(7,1)), sg.Checkbox("金额", size=(7,1)), sg.Checkbox("税率", size=(7,1))],
				[sg.Checkbox("税额", size=(7,1)),sg.Checkbox("备注", size=(7,1)),sg.Checkbox("销售方地址及电话")],
			]
		
		cam = [
				[sg.Text("-" * 90)],
				[sg.Radio('文件', group_id=2, key='文件', default=True), sg.Radio('摄像头', group_id=2, key='摄像头')],
			]
		
		input = [
				[sg.Text("-" * 90)],
				[sg.Button("开始", size=(7,1)), sg.Button("结束", size=(7,1), disabled  = True), sg.Button("保存", size=(7,1))],
			]

		output = [
				[sg.Text("-" * 90)],
				[sg.Text(('选择文件输出路径(默认路径:%s)' % ""))],
				[sg.Input(key='_DIR_', default_text="", size=(30,1)),sg.FolderBrowse()],
		]

		RightWin = [
			[sg.Frame(title="♥ OCR ♥", layout = ocr)],
			[sg.Frame(title="♥ 发票 ♥", layout = inv)],
			[sg.Frame(title="♥ 功能选择 ♥", layout = cam)],
			[sg.Frame(title="♥ input ♥", layout = input)],
			[sg.Frame(title="♥ output ♥", layout = output)],
		]
		
		MsgLog = [
			[sg.Multiline(key='MsgLog', autoscroll = True, border_width = 2, font='Song 12', size=(96, 36))],
			[sg.Button("清除", size=(7,1))]
		]
		
		LeftWin = [
			[sg.Frame(title="♥ MsgLog ♥", layout = MsgLog)],
		]

		MainWin = [
			[sg.Column(LeftWin), sg.Column(RightWin)],
		]
		

		self.form = sg.Window('{} {}'.format("Monkey Tool", "v1.1"), MainWin)
		self.camera = None
		self.ocr = None

	def get_images(self, outdir=""):
		event,values = self.form.Read(timeout = 5000)
		if event == None:
			self.form.close()
			return ("close",None)

		if values['_DIR_'] != outdir:
			self.form.FindElement('_DIR_').Update(value = outdir)

		if event == "清除":
			self.form.FindElement('MsgLog').Update("")
			return ("image", None)

		if event == "__TIMEOUT__":
			if self.camera:
				if not self.camera.is_running():
					self.form.FindElement('结束').Click()
				else:
					images,dir = self.camera.capture()
					if images == "":
						s = values['MsgLog'] + "[WARN] >>> 请拍摄照片...\n"
						self.form.FindElement('MsgLog').Update(s)
					else:
						return ("image", images + "&&" + values['_DIR_'])
			return ("image", None)
		elif event == "结束" and self.camera:
			self.form.FindElement('开始').Update(disabled  = False)
			self.form.FindElement('结束').Update(disabled  = True)
			self.camera.close()
			images,dir = self.camera.capture()
			self.camera = None
			if images == "":
				return ("image", None)
			else:
				return ("image", images + "&&" + values['_DIR_'])
		elif event == "开始":
			s = values["MsgLog"] + ("[INFO] >>> <开始>按钮被选择 ...\n") 
			self.form.FindElement('MsgLog').Update(s)
			if values['文件']:
				images,dir = image_windows_show(values['_DIR_'])
				if images == "" or images is None:
					s = s + "[WARN] >>> 未选择任何文件... 请选择\n"
					self.form.FindElement('MsgLog').Update(s)
					return ("image",None)
				else:
					return ("image", images + "&&" + dir)
			elif values['摄像头']:
				self.form.FindElement('开始').Update(disabled  = True)
				self.form.FindElement('结束').Update(disabled  = False)
				if self.camera is None:
					self.camera = capture.win_camera()
				images,dir = self.camera.capture()
				if images == "":
					return ("image",None)
				else:
					return ("image", images + "&&" + values['_DIR_'])
		elif event == "保存":
			return ("save", None)
		else:
			return ("save", None)
	
	def API_KEY(self):
		event,values = self.form.Read(timeout = 0)
		return values['API_KEY']
	
	def SECRET_KEY(self):
		event,values = self.form.Read(timeout = 0)
		return values['SECRET_KEY']
	
	def ocr(file=""):
		return self.ocr.get(file)

	def update_msg(self, str=""):
		event,values = self.form.Read(timeout = 0)
		self.form.FindElement('MsgLog').Update(values['MsgLog'] + str)

	def connect(self):
		while True:
			event,values = self.form.Read(timeout = 2000)
			if os.path.isfile(ConfigKeys):
				f = open(ConfigKeys)
				local_API_KEY = f.readline().replace("\n","")
				local_SECRET_KEY = f.readline().replace("\n","")
				f.close()
				if local_API_KEY and local_SECRET_KEY:
					self.form.FindElement('API_KEY').Update(value=local_API_KEY)
					self.form.FindElement('SECRET_KEY').Update(value=local_SECRET_KEY)
			try:
				urllib.request.urlopen('https://www.baidu.com')
			except:
				self.form.FindElement('MsgLog').Update(values['MsgLog'] + "[ERROR] >>> 请检查你的网络 ...\n")
				continue

			local_API_KEY = self.API_KEY()
			local_SECRET_KEY = self.SECRET_KEY()
			if not (local_API_KEY.isalnum() and local_SECRET_KEY.isalnum()):
				self.form.FindElement('MsgLog').Update(values['MsgLog'] + "[ERROR] >>> 请输入正确的KEY ...\n")
				continue
			else:
				tocr = ocr.ocr()
				if not tocr.install(API_KEY=local_API_KEY, SECRET_KEY=local_SECRET_KEY):
					self.form.FindElement('MsgLog').Update(values["MsgLog"] + "[ERROR] >>> OCR 连接失败 ...\n")
					continue
				else:
					self.ocr = tocr
					f = open(ConfigKeys,'w+',encoding='utf-8')
					f.write(local_API_KEY + "\n")
					f.write(local_SECRET_KEY + "\n")
					f.close()
					self.form.FindElement('MsgLog').Update(values["MsgLog"] + "[INFO] >>> OCR 连接成功 ...\n")
					break