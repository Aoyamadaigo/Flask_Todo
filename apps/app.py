"""
app.py

flaskはappsフォルダは以下のapp.pyファイルを探し,appを実行する。
__init__.pyでアプリの初期を行い、app.pyで実行する
"""

from . import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
