[Setup]
AppName=Antigravity File Manager
AppVersion=1.0
DefaultDirName={autopf}\AntigravityFileManager
DefaultGroupName=Antigravity File Manager
UninstallDisplayIcon={app}\main.exe
OutputDir=.
OutputBaseFilename=AntigravityFileManager_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Antigravity File Manager"; Filename: "{app}\main.exe"
Name: "{autodesktop}\Antigravity File Manager"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,Antigravity File Manager}"; Flags: nowait postinstall skipifsilent
