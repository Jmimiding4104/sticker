import subprocess

def build_exe():
    subprocess.run(["pyinstaller", "main.spec"], check=True)