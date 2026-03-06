; DSTerminal Installer Script

[Setup]
AppId={{DSTerminal}}
AppName=DSTerminal
AppVersion=2.0.59
AppPublisher=Stark Expo Tech Exchange
AppPublisherURL=https://starkexpotechexchange-mw.com
DefaultDirName={pf}\DSTerminal
DefaultGroupName=DSTerminal
LicenseFile=license.txt
OutputDir=.
OutputBaseFilename=DSTerminal_Setup_2.0.59_x64
Compression=lzma
SolidCompression=yes
WizardStyle=modern
WizardImageFile=installer_assets\logo.bmp
WizardSmallImageFile=installer_assets\logo_small.bmp
SetupIconFile=installer_assets\icon.ico
AllowNoIcons=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
UninstallDisplayIcon={app}\dsterminal.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\dsterminal_win-2.0.59_x64-amd64.exe"; DestDir: "{app}"; DestName: "dsterminal.exe"; Flags: ignoreversion

[Dirs]
Name: "{userappdata}\DSTerminal_Workspace"

[Icons]
Name: "{group}\DSTerminal"; Filename: "{app}\dsterminal.exe"; IconFilename: "installer_assets\icon.ico"
Name: "{group}\Uninstall DSTerminal"; Filename: "{uninstallexe}"
Name: "{commondesktop}\DSTerminal"; Filename: "{app}\dsterminal.exe"; IconFilename: "installer_assets\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked
Name: "addtopath"; Description: "Add DSTerminal to system PATH"; GroupDescription: "Additional options:"

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
ValueType: expandsz; ValueName: "Path"; \
ValueData: "{olddata};{app}"; \
Flags: preservestringtype; \
Tasks: addtopath; Check: NeedsAddPath(ExpandConstant('{app}'))

[Run]
Filename: "{app}\dsterminal.exe"; Description: "Launch DSTerminal"; Flags: nowait postinstall skipifsilent

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKLM,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then
    Result := True
  else
    Result := Pos(';' + Uppercase(Param) + ';',
      ';' + Uppercase(OrigPath) + ';') = 0;

// Automatic update check (simple example)
// This runs DSTerminal.exe with a special update flag after install
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    Exec(ExpandConstant('{app}\DSTerminal.exe'), '--update', '', SW_SHOW, ewNoWait, ResultCode);
  end;
end;