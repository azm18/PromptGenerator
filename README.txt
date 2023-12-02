・Python仮想環境を作成
python -m venv env

・仮想環境有効化
source env/bin/activate

・仮想環境非有効化
deactivate

・モジュールを取得&設定
pip download --dest modules --requirement requirements.txt
pip install --no-index --find-links=./modules -r requirements.txt

・以下からモデルをダウンロード
https://huggingface.co/intfloat/multilingual-e5-large/tree/main