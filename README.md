# MonkeySee
前言：

某日看见老婆拿了一大摞发票在统计,忙的不亦乐乎,

同时还发动身边的人一起帮她统计,看到她投入的样子,

我决定给她简单写个软件,多少能帮她剩去一部分辛苦，

因此就有了这个软件的诞生背景...


过程：

本人作为一名嵌入式工程师，对这种PC端的软件极为不擅长，

好在Python的粘合性很好,用到了一些基础的模块拼接一下,

基本也就完成了,核心技术就是百度的OCR,真的很强大.

软件中删除了个人账号的百度的API_KEY和SECRET_KEY.

如有需要，请自行申请.


写给懂的人：
pyinstaller.exe -D main.py -w --name MonkeySee -i ico/monkey.ico

pip install requests

pip install openpyxl

pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install pdf2image -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install PySimpleGUI -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install pyinstaller  -i https://pypi.tuna.tsinghua.edu.cn/simple

