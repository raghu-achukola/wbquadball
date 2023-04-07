import os 
import subprocess

relpath = lambda *paths: os.path.realpath(os.path.join(os.path.dirname(__file__),*paths))
SRC_DIR = relpath('models','statsheet')
DST_DIR = relpath('quadball','schema','statsheet')

for path in os.listdir(SRC_DIR):
    if path.endswith('.proto'):
        subprocess.run(
            [
                "protoc", f"-I={SRC_DIR}" ,f"--python_out={DST_DIR}",
                os.path.join(SRC_DIR,path)
            ]
        )
