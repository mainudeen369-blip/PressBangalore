# PressBangalore — UI Demo (No Backend)

Instagram-style local news **Android app** with dummy data. No API required.

## Android APK (ready to install)

**File:** [`release/PressBangalore-v1.0.apk`](release/PressBangalore-v1.0.apk)

Copy to phone → install → open **PressBangalore**

Demo login: `admin@pressbangalore.demo` / `Demo@123`

## Rebuild APK

```powershell
cd apps/web
npm run android:apk
```

Requires Android Studio + Android SDK (JDK 21 via Android Studio JBR).

## Run in browser (dev)

```powershell
cd apps/web
npm install
npm run dev
```

Open http://localhost:5173

## Demo accounts

Password for all: **Demo@123**

| Email | Role |
|-------|------|
| admin@pressbangalore.demo | Super Admin |
| reporter@pressbangalore.demo | Approved reporter |
| pending@pressbangalore.demo | Pending reporter |
| user@pressbangalore.demo | Premium user |

## Features (all mock data)

- News feed with city + language filters, stories, ads
- Reels (vertical video, swipe)
- Reporter registration, ID card, appointment letter, A/V recording
- Admin panel: approvals, ads, IR investigations, teams, role preview
- IR public tracking with timeline + consolidated reports
- Search, profile, earnings dashboard
- State persists in localStorage during demo

## Build & preview

```powershell
npm run build
npm run preview
```

## Install on phone (PWA — browser only)

Deploy to Render or run `npm run preview` on your network, then Chrome → Install app.

## Backend (later)

The `api/` folder has a .NET GraphQL API scaffold for when the client confirms. Not required for this UI demo.
