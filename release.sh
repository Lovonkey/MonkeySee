set -x
rm ./Release/MonkeySee -rf
pyinstaller.exe -D main.py -w --name MonkeySee -i ico/monkey.ico --distpath ./Release
mkdir ././Release/MonkeySee/File/
cp ./File/poppler/ ./Release/MonkeySee/File  -rf
find . -name __pycache__ | xargs rm  -r
rm ./build -r
rm MonkeySee.spec
set +x
