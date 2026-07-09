import os
import urllib.request
import shutil
import zipfile
import subprocess

PYTHON_VER = "3.10.11"
PYTHON_ZIP_URL = f"https://www.python.org/ftp/python/{PYTHON_VER}/python-{PYTHON_VER}-embed-amd64.zip"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"

def main():
    print("==================================================")
    print(" PREPARANDO ARQUIVOS PARA O INSTALADOR (INNO SETUP)")
    print("==================================================")
    
    if os.path.exists("build_installer"):
        print("Limpando build anterior...")
        shutil.rmtree("build_installer")
    os.makedirs("build_installer")
    
    print("1. Baixando o Python Embed (versão leve)...")
    zip_path = "build_installer/python_embed.zip"
    urllib.request.urlretrieve(PYTHON_ZIP_URL, zip_path)
    
    print("Extraindo Python...")
    python_dir = "build_installer/python"
    os.makedirs(python_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(python_dir)
    os.remove(zip_path) # limpar zip
    
    # Para o python embed aceitar pacotes externos, precisamos descomentar "import site" no arquivo ._pth
    pth_filename = f"python{PYTHON_VER.split('.')[0]}{PYTHON_VER.split('.')[1]}._pth"
    pth_file = os.path.join(python_dir, pth_filename)
    if os.path.exists(pth_file):
        with open(pth_file, "r") as f:
            lines = f.readlines()
        with open(pth_file, "w") as f:
            for line in lines:
                if line.strip() == "#import site":
                    f.write("import site\n")
                else:
                    f.write(line)
                    
    print("Baixando o pip...")
    pip_path = os.path.join(python_dir, "get-pip.py")
    urllib.request.urlretrieve(GET_PIP_URL, pip_path)
    
    print("Instalando pip e bibliotecas (isso pode demorar um pouco)...")
    python_exe = os.path.join(python_dir, "python.exe")
    # Instalar pip
    subprocess.run([python_exe, pip_path], check=True)
    # Instalar libs
    subprocess.run([python_exe, "-m", "pip", "install", "streamlit", "altair", "pandas"], check=True)
    
    # Remover get-pip para economizar espaço
    os.remove(pip_path)
    
    print("2. Copiando seus arquivos do projeto...")
    shutil.copy("../Stude.exe", "build_installer/Stude.exe")
    shutil.copy("../app.py", "build_installer/app.py")
    
    shutil.copytree("../assets", "build_installer/assets", dirs_exist_ok=True)
    shutil.copytree("../metodos", "build_installer/metodos", dirs_exist_ok=True)
    
    print("==================================================")
    print(" SUCESSO! A pasta 'build_installer' está pronta.")
    print(" ATENÇÃO: No seu arquivo Inno Setup (.iss), você precisa alterar para NÃO usar o instalador do python.")
    print("==================================================")

if __name__ == "__main__":
    main()
