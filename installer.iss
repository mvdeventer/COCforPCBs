; Inno Setup Script for COC Report Generator
; Creates Windows installer with version management

#define AppName "COC Report Generator"
#define AppPublisher "LHA Systems (PTY) LTD"
#define AppURL "https://github.com/Koolkop1@/COCforPCBs"
#define AppExeName "COC_Report_Generator.exe"

; Get version from file or use default
#ifndef AppVersion
  #define AppVersion "1.0.4"
#endif

[Setup]
AppId={{8F5E6A9B-1234-5678-9ABC-DEF012345678}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
; LicenseFile=LICENSE
; InfoBeforeFile=README.md
OutputDir=dist\installer
OutputBaseFilename=COC_Report_Generator_Setup_{#AppVersion}
SetupIconFile=company_logo.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "company_logo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "examples\*"; DestDir: "{app}\examples"; Flags: ignoreversion recursesubdirs createallsubdirs; Tasks: ; Languages:

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Name: "{group}\README"; Filename: "{app}\README.md"
Name: "{group}\Changelog"; Filename: "{app}\CHANGELOG.md"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
