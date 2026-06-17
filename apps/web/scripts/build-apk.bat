@echo off
set JAVA_HOME=C:\Program Files\Android\Android Studio\jbr
set ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk
cd /d "%~dp0.."
call npm run build
call npx cap sync android
cd android
call gradlew.bat assembleRelease --no-daemon
if not exist "..\..\..\..\release" mkdir "..\..\..\..\release"
copy /Y "app\build\outputs\apk\release\app-release.apk" "..\..\..\..\release\PressBangalore-v1.0.apk"
echo.
echo APK ready: release\PressBangalore-v1.0.apk
