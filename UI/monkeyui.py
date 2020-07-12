from Capture import capture
from File import f
import PySimpleGUI as sg
import cv2
import time
import os

def windows_msg_update(windows=None, key = "MsgLog", str=""):
	if not windows is None:
		tmp,msg = windows.Read(timeout=0)
		s = msg[key] + str
		windows.FindElement(key).Update(s)

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
		MainWin = [
			[sg.Text('作业内容',auto_size_text=True)],
			[sg.Radio('发票', group_id=1, key='发票', default=True), sg.Radio('合同', group_id=1,key='合同'), sg.Radio('其他', group_id=1, key='其他')], 
			[sg.Text('作业方式', auto_size_text=True)],
			[sg.Radio('文件', group_id=2, key='文件', default=True), sg.Radio('摄像头', group_id=2, key='摄像头')], 
			[sg.OK('开始', size=(10, 2)), sg.OK('保存', size=(10, 2))],
			[sg.Multiline(size=(1280, 720), key='MsgLog', autoscroll = True, border_width = 2, font='Song 12')]
		]

		self.form = sg.FlexForm('猴子读图',size=(1280, 720))
		self.form.Layout(MainWin)
		self.cap = None

	def get_images(self, outdir=""):
		if self.cap is None:
			self.cap = capture.app()

		event,values = self.form.Read()
		if event == None:
			self.form.close()
			return ("close",None)

		if event == "开始":
			s = values["MsgLog"] + ("[INFO] >>> <开始>按钮被选择 ...") 
			self.form.FindElement('MsgLog').Update(s)
	
			if values['合同'] or values['其他']:
				s = values["MsgLog"] + ("[WARN] >>>当前仅支持对发票进行操作..., 请使用正确方式")
				self.form.FindElement('MsgLog').Update(s)
				return ("image",None)
	
			if values['文件']:
				images,dir = image_windows_show(outdir)
				if images == "" or images is None:
					s = s + ("\n[WARN] >>> 未选择任何文件... 请选择")
					self.form.FindElement('MsgLog').Update(s)
					return ("image",None)
				else:
					return ("image", images + "&&" + dir)
			elif values['摄像头']:
				images,dir = self.video_windows_show(outdir, self.form)
				if images == "" or images is None:
					s = s + ("\n[WARN] >>> 未选择任何文件... 请选择")
					self.form.FindElement('MsgLog').Update(s)
					return ("image",None)
				else:
					return ("image", images + "&&" + dir)
			
		elif event == "保存":
			return ("save", None)
		else:
			return ("def", None)
		
	def update_msg(self, str=""):
		windows_msg_update(windows=self.form, str=str)

	def video_windows_show(self, outdir="", windows=None):
		index = 0
		files = None
		file = f.get_tmp_file(outdir, index)
		
		cap = self.cap 
		if not cap.isOpened():
			sg.popup(">>没有发现摄像头<<",font=("size",15))
			return (None, None)

		data=cap.capture()
		f.save(data, file)
			
		video = [
			[sg.Text(('选择文件输出路径(默认路径:%s)' % outdir))],
			[sg.Input(key='_DIR_', default_text=outdir),sg.FolderBrowse()],
			[sg.Image(filename=file, key='image')],
			[sg.OK('抓图', size=(15, 2)), sg.OK('完成', size=(15, 2))],
		]
	
		form = sg.FlexForm('猴子抓图')
		form.Layout(video)
		while True:
			event,values = form.Read(timeout=10)
			data = cap.capture()
			form['image'](data=data)
			if event == "抓图":
				index += 1
				file = f.get_tmp_file(outdir, index)
				if files is None:
					files = file
				else:
					files = files + ";" + file
				f.save(data, file)
				windows_msg_update(windows=windows, str=("[INFO] >>> 图片<%s>抓取成功" % file))
			elif event == "完成" or event == None:
				break
	
		form.close()

		if not values is None:
			return (files, values["_DIR_"])
		else:
			return (None, None)