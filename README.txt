■Pythonバージョン
python-V python3.8.10

■Python仮想環境作成
python -m venv env

■仮想環境有効化
[windows]
.\env\Scripts\activate.bat
[mac]
source env/bin/activate

■仮想環境非有効化
deactivate

■モジュールを取得&設定
pip download --dest modules --requirement requirements.txt
pip download --dest modules （モジュール名）
pip install --no-index --find-links=./modules -r requirements.txt

[開発メモ]
■以下からモデルをダウンロード
https://huggingface.co/intfloat/multilingual-e5-large/tree/main

■EXE化する際の注意点（ウイルス誤検知対策）
https://qiita.com/tru-y/items/cb3cebe9612d367dccb2
https://qiita.com/nobody_gonbe/items/5ffdd1a767c67256032e

■Pyinstallerのダウンロード
pip install pyinstaller

■PythonファイルをEXE化
pyinstaller PromptGenerator.py –-onefile –-noconsole --hidden-import=trafilatura --hidden-import=sentence-transformers

■ファイル説明
[PromptGenerator.exe]：アプリケーション実行ファイル
[config.ini]：環境変数ファイル
[PromptGenerator.bat]：Windows用Pythonアプリケーション起動バッチ
[PromptGenerator.sh]：Linux用Pythonアプリケーション起動バッチ
[PromptGenerator.py]：Pythonアプリケーション
[rag.py]：RAG関連機能
[setup.py]：モデルダウンロード
