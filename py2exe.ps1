echo "====> Create environment ====>"
py -m venv env

echo "====> Activate it ====>"
. .\env\Scripts\activate
$env:PYTHONPATH="$(pwd)"
echo "====> Install requirements ====>"
pip install -r requirements.txt

echo "====> Build exe files ====>"

echo "====> Publisher build ====>"
pyinstaller --noconfirm --onefile `
--paths .\venv\Lib\site-packages `
--console `
-F ".\src\confpoint\publisher\push.py" `
--distpath "bin" --name "confpoint-publisher"

echo "====> Uploader build ====>"
pyinstaller --noconfirm --onefile `
--paths .\venv\Lib\site-packages `
--console -F ".\src\confpoint\uploader\oneloader.py" `
--distpath "bin" --name "confpoint-uploader"

echo "====> Download build ====>"
pyinstaller --noconfirm --onefile `
--paths .\venv\Lib\site-packages `
--console `
-F ".\src\confpoint\downloader\onedownloader.py" `
--distpath "bin" --name "confpoint-downloader"

echo "====> Check bin directory"
