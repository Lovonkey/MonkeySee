# coding=utf-8
from DuniangOCR import ocr
from Execle import invoice
from UI import monkeyui
from File import f
import time
import os

#ydYHklBZz9jeDUTN8yZCdZo7
#maTlUB60yXfE1drUSA0mvvxpf7R4xAHI
if __name__ == '__main__':
	win = monkeyui.MainWindow()
	execl = invoice.invoice()
	keys = execl.get_keys()
	win.connect()
	
	while True:
		file = execl.get_file_name()
		outdir="\\".join(file.split("\\")[0:-1])
		event, images = win.get_images(outdir)
		if event == "close":
			break
		elif event == "save":
			execl.fill_cell()
			execl.save()
			file = execl.get_file_name()
			win.update_msg(("[INFO] >>> 文件路径如下:\n    %s") % file)
		elif event == "image":
			if images is None:
				continue

			files = images.split("&&")[0]
			dir = images.split("&&")[1]
			if (os.path.exists(dir)):
				if (outdir != dir):
					execl.fix_dir(dir)

			for file in files.split(";"):
				nfiles = f.refix(file, outdir)
				if nfiles is None:
					win.update_msg(("[ERRO] >>> 转换<%s>失败 ...") % f.realname(file))
					continue
				else:
					win.update_msg(("[INFO] >>> 转换<%s> --> <%s> 成功 ...") % (f.realname(file), f.realname(nfiles)))

				for nfile in nfiles.split(";"):
					ret, words_result = win.ocr.get(nfile)
					if ret == "success":
						row = execl.get_auto_write_row()
						for i, key in enumerate(keys, 1):
							res = words_result[key]
							if isinstance(res,list):
								for j, r in enumerate(res):
									execl.write(row = row + j, column = i, value = r["word"])
							else:
								execl.write(row = row, column = i, value = res)
						win.update_msg(("[INFO] >>> 统计<%s (%s)> 完成 ...") % (f.realname(file), f.realname(nfile)))
					elif ret == "same":
						win.update_msg(("[ERRO] >>> <%s (%s)> 和 <%s> 是相同的发票 ...") % (f.realname(file), f.realname(nfile), words_result))
					elif ret == "failed":
						win.update_msg(("[ERRO] >>> 统计<%s (%s)> 失败 ...") % (f.realname(file), f.realname(nfile)))
					else:
						win.update_msg(("[ERRO] >>> 统计<%s (%s)> 失败(不明返回值) ...") % (f.realname(file), f.realname(nfile)))
		else:
			win.update_msg(("[Warn] >>> 不存在的消息(%s)") % event)
	
	execl.fill_cell()
	execl.save()