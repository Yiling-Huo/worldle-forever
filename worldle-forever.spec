# -*- mode: python ; coding: utf-8 -*-

# py -m PyInstaller worldle-forever.spec

a = Analysis(
    ['worldle-forever.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["altgraph","anyio","argon2-cffi","argon2-cffi-bindings","asttokens","attrs","Babel","backcall","beautifulsoup4","bleach","certifi","cffi","charset-normalizer","click","colorama","cx-Freeze","cx-Logging","debugpy","decorator","defusedxml","entrypoints","et-xmlfile","executing","ffmpeg-python","ftfy","future","google-ngram-downloader","idna","ipykernel","ipython","ipython-genutils","jedi","Jinja2","joblib","json5","jsonschema","jupyter-client","jupyter-core","jupyter-server","jupyterlab","jupyterlab-pygments","jupyterlab-server","langcodes","lief","MarkupSafe","matplotlib-inline","mistune","msgpack","nbclassic","nbclient","nbconvert","nbformat","nest-asyncio","nltk","notebook","notebook-shim","openpyxl","packaging","pandocfilters","parso","pefile","pickleshare","pip","prometheus-client","prompt-toolkit","psutil","pure-eval","py","pycparser","pydub","Pygments","pyinstaller","pyinstaller-hooks-contrib","pyparsing","pypinyin","pyrsistent","python-dateutil","pytz","pywin32","pywin32-ctypes","pywinpty","pyzmq","regex","requests","Send2Trash","setuptools","six","smart-open","sniffio","soupsieve","stack-data","terminado","testpath","tornado","tqdm","traitlets","urllib3","wcwidth","webencodings","websocket-client","wget","wikipedia","wordfreq","you-get", "numpy", "gensim"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='worldle-forever',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
    icon='icon.ico',
)
