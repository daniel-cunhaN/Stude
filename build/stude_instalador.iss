[Setup]
; Informações do aplicativo
AppName=Stude
AppVersion=2.2.0
AppPublisher=Stude
; Onde será instalado (Program Files)
DefaultDirName={autopf}\Stude
DefaultGroupName=Stude
; Pasta de saída e nome do instalador gerado
OutputDir=.\Output
OutputBaseFilename=StudeSetup-2.2.0
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
; Opções visuais
DisableProgramGroupPage=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Copia tudo de dentro de build_installer (incluindo Stude.exe, app.py, pasta python, assets, metodos) para a raiz do programa
Source: "build_installer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Cria atalhos no Menu Iniciar e na Área de Trabalho apontando para o Stude.exe
Name: "{group}\Stude"; Filename: "{app}\Stude.exe"
Name: "{autodesktop}\Stude"; Filename: "{app}\Stude.exe"; Tasks: desktopicon

[Run]
; Permite que o usuário abra o aplicativo logo após a instalação
Filename: "{app}\Stude.exe"; Description: "{cm:LaunchProgram,Stude}"; Flags: nowait postinstall skipifsilent
