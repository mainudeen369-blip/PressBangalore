# PressBangalore — Android APK

## Install the app

**APK file:** [`release/PressBangalore-v1.1.apk`](../release/PressBangalore-v1.1.apk) (back button fix)

1. Copy the APK to your Android phone
2. Open it → allow **Install from unknown sources** if prompted
3. Install and open **PressBangalore**

**Demo login:** `admin@pressbangalore.demo` / `Demo@123`

## Rebuild APK

Requires Android Studio (for JDK 21) and Android SDK.

```powershell
cd apps/web
npm run android:apk
```

Output: `release/PressBangalore-v1.0.apk`

## App details

| | |
|---|---|
| Package | `com.pressbangalore.demo` |
| Name | PressBangalore |
| Min Android | 7.0 (API 24) |
| Data | All dummy/mock — works offline |
