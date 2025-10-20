!define APP_NAME "SuperMario2005"
!define APP_VERSION "1.0"
!define COMPANY_NAME "GameDeveloper"
!define INSTALL_DIR "$PROGRAMFILES\\${COMPANY_NAME}\\${APP_NAME}"

; Output installer name
OutFile "${APP_NAME}_Installer.exe"

; Default installation directory
InstallDir ${INSTALL_DIR}

; Request application privileges for Windows Vista and higher
RequestExecutionLevel user

Page directory
Page instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  ; Copy files from the distribution folder
  ; Assumes the installer is run from the folder that contains the 'SuperMario2005' folder
  File /r "SuperMario2005\\*.*"

  ; Create shortcuts
  CreateShortCut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\SuperMario2005.exe"
  CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\SuperMario2005.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\\SuperMario2005.exe"
  RMDir /r "$INSTDIR"
  Delete "$DESKTOP\\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk"
  RMDir "$SMPROGRAMS\\${APP_NAME}"
SectionEnd
