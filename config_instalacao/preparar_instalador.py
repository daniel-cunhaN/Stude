import os
import urllib.request
import shutil

PYTHON_VER = "3.10.11"
PYTHON_EXE_URL = f"https://www.python.org/ftp/python/{PYTHON_VER}/python-{PYTHON_VER}-amd64.exe"

def main():
    print("==================================================")
    print(" PREPARANDO ARQUIVOS PARA O INSTALADOR (INNO SETUP)")
    print("==================================================")
    
    if os.path.exists("build_installer"):
        print("Limpando build anterior...")
        shutil.rmtree("build_installer")
    os.makedirs("build_installer")
    
    print("1. Baixando o Instalador do Python (Isso será embutido no seu setup)...")
    urllib.request.urlretrieve(PYTHON_EXE_URL, "build_installer/python_installer.exe")
    
    print("2. Copiando seus arquivos do projeto...")
    shutil.copy("Stude.exe", "build_installer/Stude.exe")
    shutil.copy("app.py", "build_installer/app.py")
    
    # Criar requirements.txt para o instalador rodar
    with open("build_installer/requirements.txt", "w") as f:
        f.write("streamlit\naltair\npandas\n")
        
    shutil.copytree("assets", "build_installer/assets", dirs_exist_ok=True)
    shutil.copytree("metodos", "build_installer/metodos", dirs_exist_ok=True)
    
    print("==================================================")
    print(" SUCESSO! A pasta 'build_installer' está pronta.")
    print(" Agora compile o arquivo 'stude_instalador.iss' no Inno Setup.")
    print("==================================================")

if __name__ == "__main__":
    main()
