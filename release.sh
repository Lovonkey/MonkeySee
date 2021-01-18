set -x
rm ./Release/MonkeySee -rf
pyinstaller.exe -w -D main.py --name MonkeySee -i ico/monkey.ico --distpath ./Release
mkdir ./Release/MonkeySee/File/
cp ./File/poppler/ ./Release/MonkeySee/File  -rf
mkdir ./Release/MonkeySee/Conf/
touch ./Release/MonkeySee/Conf/key.txt
find . -name __pycache__ | xargs rm  -r
rm ./build -r
rm MonkeySee.spec
set +x
