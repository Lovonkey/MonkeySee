import os
import sys
from pdf2image import convert_from_path,convert_from_bytes
from PIL import Image
 
def get_tmp_file(outdir = "", index = 0, format = "jpg"):
	dir = os.path.join(outdir, "发票图片")
	if not os.path.exists(dir):
		os.makedirs(dir) 
	return os.path.join(dir, ("image%d.%s" % (index, format)))

def pdf2png(file="", dir=""):
	nfiles = None
	bdir = "\\".join(os.path.realpath(__file__).split("\\")[0:-1]) + "\\poppler\\bin"
	if not os.path.exists(bdir):
		return nfiles

	images = convert_from_path(file, dpi=150, poppler_path=bdir)
	for j, i in enumerate(images, 1):
		nfile = get_tmp_file(dir, index = j, format="png")
		i.save(nfile, "png")
		if nfiles is None:
			nfiles = nfile
		else:
			nfiles = nfiles + ";" + nfile
	return nfiles

def imageresize(file="", dir=""):
	nfile = get_tmp_file(dir)
	img = Image.open(file)
	w = int(img.size[0] * 1048576 / os.path.getsize(file))
	h = int(img.size[1] * 1048576 / os.path.getsize(file))
	out = img.resize((w, h))
	out.save(nfile)
	return nfile

def refix(file="", dir=""):
	if not os.path.exists(dir):
		return None

	if os.path.exists(file):
		type = file.split(".")[-1:]
		if ("".join(type) == "pdf"):
			nfile = pdf2png(file, dir)
		else: 
			size = os.path.getsize(file)
			if size > (2 * 1024 * 1024):		#2M
				nfile = imageresize(file, dir)
			else:
				nfile = file

		return nfile
	else:
		return None

def save(data, file):
		f = open(file, "wb+")
		f.write(data)
		f.close()

def realname(files = ""):
	rfile = None
	for file in files.split(";"):
		if not os.path.exists(file):
			return files
		
		if rfile == None:
			rfile = "".join(file.replace('\\', '/').split("/")[-1:])
		else:
			rfile = rfile + " " + "".join(file.replace('\\', '/').split("/")[-1:])

	return rfile