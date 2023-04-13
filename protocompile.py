import os 
import subprocess

relpath = lambda *paths: os.path.realpath(os.path.join(os.path.dirname(__file__),*paths))



def compile_protos(src_path:str, dest_path:str) -> None:
    for path in os.listdir(src_path):
        if path.endswith('.proto'):
            subprocess.run(
                [
                    "protoc", f"-I={src_path}" ,f"--python_out={dest_path}",
                    os.path.join(src_path,path)
                ]
            )


# statsheet
compile_protos(
    relpath('models','statsheet'),
    relpath('quadball','schema','statsheet')
)


# db
compile_protos(
    relpath('models','db'),
    relpath('quadball','schema','db')
)