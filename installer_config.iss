[Setup]
AppName=CleanSweep
AppVersion=2.0
DefaultDirName={autopf}\CleanSweep
DefaultGroupName=CleanSweep
UninstallDisplayIcon={app}\CleanSweep.exe
OutputDir=.
OutputBaseFilename=CleanSweep_Setup_v2
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\CleanSweep.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CleanSweep"; Filename: "{app}\CleanSweep.exe"
Name: "{autodesktop}\CleanSweep"; Filename: "{app}\CleanSweep.exe"

[Run]
Filename: "{app}\CleanSweep.exe"; Description: "{cm:LaunchProgram,CleanSweep}"; Flags: nowait postinstall skipifsilent
