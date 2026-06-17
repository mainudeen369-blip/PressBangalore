# PressBangalore — 1-Day Demo Planning Document

**Client vision:** Instagram-style news & media platform with reporter workflows, investigations, location/language feeds, reels, ads, and multi-tier admin.

**Tech stack:** React · GraphQL · .NET Core · PostgreSQL (Neon) · Render

**Demo goal:** A polished, navigable product that *feels* complete — core flows work end-to-end; advanced modules are represented with realistic UI + seed data.

**Target delivery:** 1 day (demo-ready deploy on Render)

---

## 1. Executive Summary

| Aspect | Demo scope (Day 1) | Post-demo (Phase 2+) |
|--------|-------------------|----------------------|
| **User app** | Feed, posts, reels, profile, location/language filters | Full monetization, notifications, offline |
| **Reporter portal** | Register → pending → approved flow, status, media upload | ID card PDF generation, appointment letters |
| **Admin panel** | Super Admin / Admin / Sub Admin roles, approvals, dashboard | Full RBAC, audit logs, bulk ops |
| **Investigations (IR)** | IR create, trackable number, IO assignment, team list | Team consolidation, report merging |
| **Ads** | Ad slots in feed + admin CRUD | Targeting, billing, analytics |
| **Media** | Image/video/audio on posts & reels (upload + playback) | Transcoding, CDN, live stream |

The demo prioritizes **visual polish** (Instagram-like UX) and **3–4 hero journeys** that the client can click through live.

---

## 2. Hero Demo Journeys (Must Work Live)

### Journey A — Consumer (Instagram-like)
1. Land on **location + language** selector (e.g. Bangalore / Kannada, English).
2. Scroll **news feed** — mix of text, image, audio snippet, video.
3. Open **Reels** tab — vertical short videos (swipe, like, comment UI).
4. View **profile** — posts grid, follower counts, premium badge (mock).

### Journey B — Reporter
1. **Register** as reporter (name, area, language, ID upload placeholder).
2. See **status: Pending** on reporter dashboard.
3. Admin approves → status **Approved** → reporter can **create news post** with photo/video/audio.

### Journey C — Admin
1. Login as **Super Admin** → dashboard (users, reporters pending, posts, earnings mock chart).
2. **Approve/reject** reporter from queue.
3. **Approve/reject** news posts (approval flow).
4. Switch role preview: **Admin** / **Sub Admin** (limited menus).

### Journey D — Investigation (IR)
1. Create **IR** with auto-generated **trackable IR number** (e.g. `IR-BLR-2026-00042`).
2. Assign **IO** (Investigation Officer) and **team**.
3. Public **track IR** page: enter number → status timeline (mock stages).

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Render (Hosting)                          │
├─────────────────┬─────────────────────┬─────────────────────────┤
│  React SPA      │  .NET Core API      │  Neon PostgreSQL        │
│  (Static Site)  │  HotChocolate GQL   │  (Managed Postgres)     │
│  Vite + TS      │  REST for uploads   │                         │
└────────┬────────┴──────────┬──────────┴──────────┬────────────┘
         │                   │                       │
         │    GraphQL        │    EF Core            │
         └──────────────────►├──────────────────────►│
                             │                       │
                    File storage (demo):              │
                    Render disk / Cloudinary          │
                    (optional free tier)              │
```

### Repos / folders (monorepo)

```
PressBangalore/
├── apps/
│   ├── web/                 # React — consumer + reels (Instagram UX)
│   ├── admin/               # React — approval & analytics dashboard
│   └── reporter/            # React — reporter registration & posts (or routes in web)
├── api/
│   └── PressBangalore.Api/  # .NET 8, HotChocolate GraphQL, JWT auth
├── docs/
│   └── PLANNING.md
└── render.yaml              # Blueprint deploy
```

**Day-1 simplification:** Single React app with route groups (`/`, `/reels`, `/reporter`, `/admin`, `/track-ir`) instead of three separate SPAs — faster to ship, same demo impact.

### GraphQL vs REST split

| Use GraphQL | Use REST |
|-------------|----------|
| Feed, posts, users, reporters, IR queries/mutations | File upload (multipart) |
| Admin lists, approvals | Health check |
| Dashboard aggregates | Webhook stubs (future) |

---

## 4. Data Model (PostgreSQL / Neon)

### Core entities

```
User
  id, email, password_hash, display_name, avatar_url
  role: Consumer | Premium | Reporter | SubAdmin | Admin | SuperAdmin
  is_premium, language_pref, location_lat, location_lng, city, created_at

ReporterProfile
  user_id (FK), area, beat, languages[], status: Pending|Approved|Rejected|Suspended
  id_document_url, appointment_letter_url (nullable demo)
  approved_by, approved_at

NewsPost
  id, author_id, title, body, type: News|Reel|Business|Entertainment|Professional
  media: [{ type: image|video|audio, url, thumbnail_url }]
  location_city, language, status: Draft|PendingApproval|Published|Rejected
  likes_count, views_count, created_at

Reel
  id, post_id (or embedded in NewsPost with type=Reel)
  video_url, duration_sec, category

Advertisement
  id, title, image_url, link_url, slot: FeedTop|FeedInline|Reels
  active_from, active_to, target_city, target_language

Investigation (IR)
  id, ir_number (unique, indexed), title, description
  status: Open|Assigned|InProgress|Consolidated|Closed
  io_user_id, created_at

IRTeam / IRAssignment
  ir_id, team_id, role, assigned_at

Team
  id, name, region, member_ids[]

IRReport (consolidation stub)
  ir_id, team_id, report_body, submitted_at

ApprovalLog
  entity_type, entity_id, action, actor_id, note, created_at
```

### IR number format (demo)

`IR-{CITY_CODE}-{YEAR}-{SEQUENCE}` → `IR-BLR-2026-00001`  
Generated in API on create; exposed via GraphQL + public track query.

---

## 5. API Design (.NET Core + HotChocolate)

### Packages
- `HotChocolate.AspNetCore` — GraphQL
- `Microsoft.EntityFrameworkCore` + `Npgsql.EntityFrameworkCore.PostgreSQL`
- `Microsoft.AspNetCore.Authentication.JwtBearer`
- `BCrypt.Net-Next` — password hashing

### Sample GraphQL surface (demo)

**Queries**
- `feed(location, language, limit, cursor)` — paginated posts + inline ads
- `reels(limit, cursor)`
- `me` — current user + reporter profile
- `reportersPending` — admin only
- `postsPendingApproval` — admin only
- `dashboardStats` — counts + mock earnings series
- `trackIr(irNumber)` — public, no auth
- `investigation(id)` — admin/IO

**Mutations**
- `registerUser`, `login`
- `registerReporter(input)`
- `createPost(input)`, `createReel(input)`
- `approveReporter(id)`, `rejectReporter(id, reason)`
- `approvePost(id)`, `rejectPost(id)`
- `createInvestigation(input)`, `assignIo(irId, userId)`, `assignTeam(irId, teamId)`
- `createAd(input)`, `updateAd(id)` — admin

### Auth & roles (JWT claims)

| Role | Demo permissions |
|------|------------------|
| Consumer | Feed, reels, profile |
| Premium | + badge, mock “earnings” on dashboard |
| Reporter | + create posts (pending approval) |
| SubAdmin | + approve posts only |
| Admin | + approve reporters, ads, IR assign |
| SuperAdmin | + user role management, all stats |

---

## 6. Frontend (React — Instagram-inspired UX)

### Stack
- **Vite + React 18 + TypeScript**
- **TanStack Query** — GraphQL via `graphql-request` or Apollo Client
- **React Router v6**
- **Tailwind CSS** + **shadcn/ui** (or similar) — fast, modern components
- **Framer Motion** — reel transitions, feed animations

### Design language (client expectation)
- Bottom nav on mobile: Home · Reels · + · Search · Profile
- Stories row (optional demo: static avatars)
- Card feed: media-first, engagement bar (like, comment, share)
- Reels: full-screen vertical, gesture-friendly
- Dark/light mode toggle (premium feel)
- Kannada + English UI strings (i18n ready, 2 languages in demo)

### Key screens

| Route | Screen |
|-------|--------|
| `/` | News feed (location/language chips at top) |
| `/reels` | Vertical video reel viewer |
| `/post/:id` | Post detail + audio/video player |
| `/login`, `/register` | Auth |
| `/reporter/register` | Reporter onboarding form |
| `/reporter/dashboard` | Status, create post, my posts |
| `/admin` | Dashboard home |
| `/admin/reporters` | Approval queue |
| `/admin/posts` | Post approval queue |
| `/admin/ads` | Ad panel |
| `/admin/ir` | IR list + create/assign |
| `/track` | Public IR tracker |
| `/profile` | User profile + mock analytics |

### Media handling (demo)
- Upload to API → store under `wwwroot/uploads` or Cloudinary
- Accept: jpg, png, mp4, mp3 (validate MIME)
- Video: HTML5 `<video>`; audio: waveform-style player UI
- Reels: same video pipeline, max ~60s for demo

---

## 7. Feature Matrix — Demo vs Later

| Feature | Day-1 demo | Notes |
|---------|------------|-------|
| News feed | ✅ | Location + language filter on query |
| News post + attachments | ✅ | Image, video, audio |
| Reporter registration | ✅ | Form + file placeholder |
| Reporter approval | ✅ | Admin queue |
| User / Premium user | ✅ | Badge + dashboard mock earnings |
| Approval flow (posts) | ✅ | Pending → published |
| Approval admin site | ✅ | `/admin` routes |
| Reporter status | ✅ | Pending/Approved/Rejected UI |
| Reporter ID cards | 🔶 | UI card preview with seed data; PDF gen later |
| Appointment letters | 🔶 | Upload field + sample PDF link |
| Reporter A/V recordings | ✅ | Upload on post/profile |
| IR + trackable number | ✅ | Generate + public track page |
| IO assignment | ✅ | Dropdown assign |
| Teams + consolidation | 🔶 | Team list + “consolidated report” mock view |
| Advertisement panel | ✅ | Admin CRUD + feed injection |
| Role hierarchy | ✅ | 3 admin tiers + reporter + user |
| Profile & analytics dashboard | ✅ | Charts with seed/mock data |
| Reels | ✅ | Vertical feed, core interactions |
| Instagram UX | ✅ | Primary design target |

Legend: ✅ fully demoable · 🔶 UI + seed data, limited backend

---

## 8. 1-Day Execution Schedule

Assume **~10–12 focused hours** (or 2 devs × 6h).

| Block | Time | Tasks |
|-------|------|-------|
| **0. Setup** | 0:00–1:00 | Repo scaffold, Neon DB, .NET API skeleton, React + Tailwind, `render.yaml` |
| **1. Backend core** | 1:00–3:00 | EF models, migrations, JWT auth, seed users (all roles) |
| **2. GraphQL** | 3:00–5:00 | Feed, posts, reporter mutations, approvals, IR create/track |
| **3. Uploads** | 5:00–5:45 | Multipart endpoint, static file serving |
| **4. Consumer UI** | 5:45–8:00 | Feed, reels, post detail, profile, i18n chips |
| **5. Reporter UI** | 8:00–9:00 | Register, dashboard, create post with media |
| **6. Admin UI** | 9:00–10:30 | Dashboard, approval queues, ads, IR management |
| **7. IR track + polish** | 10:30–11:15 | Public tracker, loading states, empty states |
| **8. Deploy** | 11:15–12:00 | Render web + API + env vars, smoke test |
| **Buffer** | 12:00+ | Demo script rehearsal, hotfix |

### Seed data (critical for demo)
- 20+ feed posts (mixed media types)
- 8–10 reels
- 5 reporters (2 pending, 3 approved)
- 3 IR records at different statuses
- 2–3 active ads
- 1 Super Admin, 1 Admin, 1 Sub Admin test accounts

---

## 9. Deployment (Render)

### Services

| Service | Type | Notes |
|---------|------|-------|
| `pressbangalore-api` | Web Service | .NET 8, Dockerfile or `dotnet publish` |
| `pressbangalore-web` | Static Site | `npm run build` → `dist` |
| Database | **Neon** (external) | Connection string in Render env |

### Environment variables

**API**
```
DATABASE_URL=postgresql://...@neon.tech/...
JWT_SECRET=<strong-secret>
JWT_ISSUER=PressBangalore
CORS_ORIGINS=https://pressbangalore-web.onrender.com
ASPNETCORE_ENVIRONMENT=Production
```

**Web**
```
VITE_GRAPHQL_URL=https://pressbangalore-api.onrender.com/graphql
VITE_API_URL=https://pressbangalore-api.onrender.com
```

### `render.yaml` (blueprint sketch)

```yaml
services:
  - type: web
    name: pressbangalore-api
    runtime: docker
    dockerfilePath: ./api/Dockerfile
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: JWT_SECRET
        generateValue: true
  - type: web
    name: pressbangalore-web
    runtime: static
    buildCommand: cd apps/web && npm ci && npm run build
    staticPublishPath: apps/web/dist
    envVars:
      - key: VITE_GRAPHQL_URL
        value: https://pressbangalore-api.onrender.com/graphql
```

**Neon:** Create project → copy pooled connection string → run EF migrations on deploy (`dotnet ef database update` in release command or manual once).

---

## 10. Demo Script (Client Presentation — ~15 min)

1. **Vision** (1 min) — “Instagram meets local news + verified reporters.”
2. **Consumer** (4 min) — Language/location → feed → open video post → Reels → like/comment UI.
3. **Reporter** (3 min) — Register → show pending → switch to admin → approve → reporter creates post with video.
4. **Admin** (4 min) — Dashboard stats → post approval → ad slot → role differences (Sub Admin vs Admin).
5. **Investigation** (2 min) — Create IR → show number → assign IO/team → public track page.
6. **Roadmap** (1 min) — ID card PDF, team report consolidation, payments, push notifications.

### Test accounts (share with client)

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@pressbangalore.demo | Demo@123 |
| Reporter (approved) | reporter@pressbangalore.demo | Demo@123 |
| Reporter (pending) | pending@pressbangalore.demo | Demo@123 |
| Consumer | user@pressbangalore.demo | Demo@123 |

---

## 11. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Render cold start | Keep API warm before demo; mention paid tier for production |
| Large video uploads on free tier | Limit file size (e.g. 25MB), use short seed clips |
| 1-day scope creep | Stick to hero journeys; stub ID cards & consolidation |
| Neon connection limits | Use pooled connection string |
| GraphQL learning curve | HotChocolate code-first; minimal schema |

---

## 12. Phase 2 Backlog (Post-Demo)

1. PDF generation — reporter ID cards & appointment letters
2. IR team report consolidation workflow
3. Real earnings & premium subscriptions
4. Push notifications (FCM)
5. Advanced ad targeting & billing
6. Content moderation / AI assist
7. CDN for media (Cloudflare R2 / Cloudinary)
8. Mobile apps (React Native) sharing GraphQL API
9. Full audit trail & compliance exports
10. Multi-city expansion & CMS for editors

---

## 13. Success Criteria for Day-1 Demo

- [ ] Live URL on Render (HTTPS)
- [ ] User can browse feed filtered by city + language
- [ ] Reels page with vertical video UX
- [ ] Reporter register → admin approve → post appears after approval
- [ ] Admin dashboard with role-based menus
- [ ] IR created with trackable number + public status page
- [ ] Ads visible in feed
- [ ] Premium badge + profile analytics (mock data acceptable)
- [ ] Polished mobile-responsive UI comparable to modern social apps
- [ ] No critical errors in happy-path demo script

---

## 14. Immediate Next Steps

1. **Confirm** demo city/languages (default: Bangalore, Kannada + English).
2. **Create** Neon PostgreSQL project and store `DATABASE_URL`.
3. **Scaffold** monorepo: `api/` + `apps/web/`.
4. **Implement** per schedule §8 — backend first, then UI on seed data.
5. **Deploy** to Render and run demo script once end-to-end.

---

*Document version: 1.0 · Date: 2026-06-15 · Stack: React, GraphQL, .NET Core, Neon Postgres, Render*
