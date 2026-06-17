"""
Generate PressBangalore Product Specification & Flow Document (PDF)
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from flow_ui_mockups import (
    SystemArchitectureDiagram,
    build_flow_sections,
    get_flow_summary_table,
)
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = r"c:\HajaWorkingFolder\PressBangalore\docs\PressBangalore-Product-Specification-Flow.pdf"

# A4 with 2cm margins on each side
CONTENT_WIDTH = A4[0] - 4 * cm

# Brand colors
PRIMARY = colors.HexColor("#1a365d")
ACCENT = colors.HexColor("#c53030")
MUTED = colors.HexColor("#4a5568")
LIGHT_BG = colors.HexColor("#edf2f7")


def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontSize=28,
            leading=34,
            textColor=PRIMARY,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            parent=base["Normal"],
            fontSize=14,
            leading=20,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontSize=18,
            leading=24,
            textColor=PRIMARY,
            spaceBefore=16,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontSize=13,
            leading=18,
            textColor=ACCENT,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontSize=11,
            leading=15,
            textColor=PRIMARY,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.black,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontSize=10,
            leading=14,
            leftIndent=14,
            bulletIndent=0,
            spaceAfter=3,
        ),
        "flow_step": ParagraphStyle(
            "FlowStep",
            parent=base["Normal"],
            fontSize=10,
            leading=14,
            leftIndent=8,
            spaceAfter=4,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.white,
            fontName="Helvetica-Bold",
            alignment=TA_LEFT,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.black,
            fontName="Helvetica",
            alignment=TA_LEFT,
        ),
    }
    return styles


def bullet_list(items, style):
    return [Paragraph(f"&bull; {item}", style) for item in items]


def flow_block(title, steps, styles):
    elements = [Paragraph(title, styles["h3"])]
    for i, step in enumerate(steps, 1):
        elements.append(Paragraph(f"<b>Step {i}.</b> {step}", styles["flow_step"]))
    elements.append(Spacer(1, 6))
    return elements


def _cell_paragraph(text, styles, is_header=False):
    """Wrap table cell text in Paragraph so ReportLab wraps within column width."""
    if isinstance(text, Paragraph):
        return text
    safe = html.escape(str(text))
    style = styles["table_header"] if is_header else styles["table_cell"]
    return Paragraph(safe, style)


def make_table(styles, data, col_widths=None):
    if col_widths is None:
        col_count = len(data[0]) if data else 1
        col_widths = [CONTENT_WIDTH / col_count] * col_count

    # Wrap every cell in Paragraph for proper word wrapping
    wrapped = []
    for row_idx, row in enumerate(data):
        wrapped.append(
            [_cell_paragraph(cell, styles, is_header=(row_idx == 0)) for cell in row]
        )

    t = Table(wrapped, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0] / 2, 15 * mm, f"PressBangalore Product Specification  |  Page {doc.page}")
    canvas.restoreState()


def build_document():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2.2 * cm,
        title="PressBangalore Product Specification & Flow",
        author="Haja Mainudeen",
    )
    story = []

    # ---- COVER ----
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph("PressBangalore", styles["cover_title"]))
    story.append(Paragraph("Digital News & Media Platform", styles["cover_sub"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(
        Paragraph(
            "<b>Product Specification, Module Flows &amp; Development Scope</b>",
            styles["cover_sub"],
        )
    )
    story.append(Spacer(1, 1.5 * cm))
    story.append(
        Paragraph(
            "Prepared for client review based on demo application, "
            "discovery discussions, and media-house best practices.",
            styles["cover_sub"],
        )
    )
    story.append(Spacer(1, 1.2 * cm))
    story.append(
        Paragraph(
            "<b>Prepared by:</b> Haja Mainudeen",
            styles["cover_sub"],
        )
    )
    story.append(
        Paragraph(
            "Full Stack Developer &nbsp;|&nbsp; 7 Years Experience",
            styles["cover_sub"],
        )
    )
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph("Document Version: 1.2", styles["cover_sub"]))
    story.append(Paragraph("Date: June 2026", styles["cover_sub"]))
    story.append(Paragraph("Status: Demo delivered — Full production scope + visual UI flows", styles["cover_sub"]))
    story.append(PageBreak())

    # ---- 1. EXECUTIVE SUMMARY ----
    story.append(Paragraph("1. Executive Summary", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "PressBangalore is a professional digital news and media platform inspired by modern "
            "social experiences (Instagram-style reels and stories) but purpose-built for verified "
            "journalism, reporter governance, editorial control, and investigative reporting. "
            "A working UI demo (web + Android APK) has been developed to showcase core journeys.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Client vision:</b> Users and reporters publish news with images, video, and audio; "
            "editorial staff review content using professional Incline/Decline workflows; "
            "investigations are tracked with unique IR numbers; location- and language-based feeds "
            "serve local audiences; advertisements monetize the platform; users communicate via "
            "in-app audio and video calls; published stories offer <b>Original</b> and <b>AI View</b> tabs "
            "(Gemini or GPT); and role-based admin panels govern the entire operation.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        make_table(
            styles,
            [
                ["Deliverable", "Status", "Description"],
                [
                    "UI Demo (Web + Android)",
                    "Completed",
                    "Full navigable demo with mock data — feed, reels, reporter, admin, IR tracking",
                ],
                [
                    "Backend API Scaffold",
                    "Ready",
                    ".NET 8 GraphQL API, PostgreSQL schema, JWT auth — awaiting integration",
                ],
                [
                    "Production Platform",
                    "Planned",
                    "Separate admin portal, real uploads, notifications, monetization, compliance",
                ],
            ],
            col_widths=[4 * cm, 2.8 * cm, CONTENT_WIDTH - 6.8 * cm],
        )
    )
    story.append(PageBreak())

    # ---- 2. PLATFORM OVERVIEW ----
    story.append(Paragraph("2. Platform Overview", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(Paragraph("2.1 Three-Portal Architecture", styles["h2"]))
    story.append(
        Paragraph(
            "For production, the platform is organized into three dedicated experiences "
            "(currently combined in the demo for speed):",
            styles["body"],
        )
    )
    story += bullet_list(
        [
            "<b>Public Web &amp; Mobile App</b> — News feed, reels, search, profile, IR public tracker, "
            "consumer registration, premium subscriptions.",
            "<b>Reporter Portal</b> — Registration, credential status, ID card, appointment letter, "
            "news submission with photo/video/audio, field recordings, earnings view.",
            "<b>Editorial Admin Portal</b> — Separate secure website for Super Admin, Admin, and Sub Admin "
            "with dedicated screens for each operational area (not mixed with consumer UI).",
        ],
        styles["bullet"],
    )
    story.append(Spacer(1, 8))
    story.append(Paragraph("2.2 Target Users", styles["h2"]))
    story.append(
        make_table(
            styles,
            [
                ["Role", "Access", "Primary Actions"],
                [
                    "Consumer (Free)",
                    "Public app",
                    "Read feed, follow stories, endorse, discuss, share, track IR",
                ],
                [
                    "Premium User",
                    "Public app",
                    "Ad-free feed, analytics, and can upload photo/video news — admin must approve before publish",
                ],
                [
                    "Reporter",
                    "Reporter portal",
                    "Submit news, upload media, view ID card & appointment letter, check status",
                ],
                [
                    "Sub Admin",
                    "Admin portal (limited)",
                    "Post review queue, reporter first-level review, basic moderation",
                ],
                [
                    "Admin",
                    "Admin portal",
                    "Reporter approval, ads, teams, IR assignment, dashboard analytics",
                ],
                [
                    "Super Admin",
                    "Admin portal (full)",
                    "User management, role assignment, system config, audit, all modules",
                ],
                [
                    "Investigation Officer (IO)",
                    "Admin / IR module",
                    "Manage assigned IR cases, submit team reports",
                ],
            ],
            col_widths=[3.2 * cm, 3.3 * cm, CONTENT_WIDTH - 6.5 * cm],
        )
    )
    story.append(PageBreak())

    # ---- 3. PROFESSIONAL TERMINOLOGY ----
    story.append(Paragraph("3. Professional Media Terminology", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Per client direction, consumer-facing and editorial language will reflect a "
            "credible newsroom — not casual social media wording. The demo currently uses "
            "social terms; production will adopt the mapping below.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        make_table(
            styles,
            [
                ["Social / Generic Term", "PressBangalore Professional Term", "Context"],
                ["Like", "Endorse", "Reader affirms credibility of a story"],
                ["Comment", "Discuss / Reader Response", "Moderated discussion thread"],
                ["Share", "Circulate", "Share via link or social channels"],
                ["Follow", "Subscribe / Follow Beat", "Follow reporter or topic"],
                ["Approve", "Incline", "Editorial acceptance — story meets standards"],
                ["Disapprove / Reject", "Decline", "Editorial rejection with reason code"],
                ["Post", "Dispatch / News Item", "Published or pending news content"],
                ["Reels", "Briefs / Field Clips", "Short-form vertical video news"],
                ["Stories", "Headlines Strip / Live Updates", "Ephemeral top stories bar"],
                ["Report (user)", "Flag / Tip-off", "Report misleading content"],
            ],
            col_widths=[3.8 * cm, 4.2 * cm, CONTENT_WIDTH - 8 * cm],
        )
    )
    story.append(Spacer(1, 10))
    story.append(Paragraph("3.1 Editorial Integrity — True News Policy", styles["h2"]))
    story += bullet_list(
        [
            "All user- and reporter-submitted content enters <b>Pending Editorial Review</b> before publication.",
            "Declined items include a reason code (unverified, defamatory, off-topic, duplicate, poor quality).",
            "Verified reporter badge displayed only after Incline approval of registration.",
            "Source attribution field mandatory for field reports; optional document upload for evidence.",
            "Fact-check status labels: <i>Verified</i>, <i>Under Review</i>, <i>Correspondent Report</i>.",
            "Correction / update log visible on edited dispatches (media-house standard practice).",
        ],
        styles["bullet"],
    )
    story.append(PageBreak())

    # ---- 4. MODULE SPECIFICATIONS ----
    story.append(Paragraph("4. Module Specifications & Brief Descriptions", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))

    modules = [
        (
            "4.1 News Feed",
            "Location- and language-filtered stream of published dispatches. Supports text, image galleries, "
            "embedded audio clips, and inline video. Headlines strip at top for breaking stories. "
            "Advertisement slots (top banner, inline, sponsored label) integrated without disrupting reading flow.",
        ),
        (
            "4.2 News Dispatch (Post Creation)",
            "Reporters and authorized users create dispatches with title, body, category (News, Business, "
            "Entertainment, Professional), city/beat, language, and media attachments. Submissions go to "
            "editorial queue. Admin Inclines to publish or Declines with feedback.",
        ),
        (
            "4.3 Briefs (Reels)",
            "Full-screen vertical short videos — field clips, explainers, or professional content. "
            "Swipe navigation, endorse/discuss/circulate actions. Separate feed tab. Supports "
            "entertainment, business, and professional categories per client vision.",
        ),
        (
            "4.4 Reporter Registration & Approval",
            "Multi-step registration: personal details, coverage area (beat), languages, ID document upload. "
            "Status lifecycle: <i>Applied &rarr; Under Review &rarr; Inclined (Approved) / Declined</i>. "
            "Email/SMS notification at each stage. Only Inclined reporters can submit dispatches.",
        ),
        (
            "4.5 Reporter Credentials",
            "Digital press ID card with photo, name, beat, validity, QR verification. "
            "Appointment letter for assigned area — viewable and downloadable as PDF. "
            "Reporter status dashboard: active, suspended, pending renewal.",
        ),
        (
            "4.6 Audio & Video Attachments",
            "News dispatches support image, video (MP4), and audio (MP3/WAV) attachments. "
            "In-app field recorder for reporters (video/audio capture). Server-side transcoding "
            "and thumbnail generation in production. Max file size and duration policies configurable.",
        ),
        (
            "4.7 User & Premium User",
            "Free consumers: read, endorse, discuss, circulate. Premium tier: ad-free feed, "
            "priority support, profile analytics, and <b>can upload photo/video news</b> from the app. "
            "All Premium submissions go to the editorial queue — admin must Incline before publish; "
            "Declined items return to the user with a reason. Subscription billing in a later release.",
        ),
        (
            "4.8 Editorial Approval Flow",
            "Central workflow engine: every dispatch and reporter application passes through review queues. "
            "Sub Admin may perform first review; Admin/Super Admin final Incline or Decline. "
            "Full audit trail: reviewer, timestamp, action, reason. Bulk actions for high-volume days.",
        ),
        (
            "4.9 Advertisement Panel",
            "Admin creates ad campaigns: image/video creative, target city, placement slot "
            "(Feed Top, Feed Inline, Briefs interstitial), schedule, active toggle. "
            "Future: impression/click analytics, advertiser self-serve portal, billing.",
        ),
        (
            "4.10 Investigation (IR) Module",
            "Create Investigation Record with auto-generated trackable number (e.g. IR-BLR-2026-00042). "
            "Assign Investigation Officer (IO) and field teams. Teams submit consolidated reports. "
            "Public tracker page: enter IR number, view status timeline and merged findings.",
        ),
        (
            "4.11 Teams & Report Consolidation",
            "Define teams (name, members, specialization). Assign teams to IR cases. "
            "Each team submits field reports; IO consolidates into master investigation summary. "
            "Status stages: Open &rarr; Assigned &rarr; In Progress &rarr; Under Review &rarr; Closed.",
        ),
        (
            "4.12 User Profile & Dashboard",
            "Profile: avatar, bio, dispatches grid, endorsements received, subscriber count. "
            "Dashboard: views over time, top dispatches, earnings (reporters/premium creators), "
            "engagement breakdown. Charts and export for admin analytics.",
        ),
        (
            "4.13 Search & Discovery",
            "Full-text search across dispatches, reporters, tags. Trending topics for city. "
            "Quick link to IR public tracker. Filter by language, category, date.",
        ),
        (
            "4.14 In-App Communication (Audio & Video Calls)",
            "Users, reporters, and editorial staff can communicate directly within the platform. "
            "One-to-one and group audio calls; one-to-one and group video calls; call from profile, "
            "dispatch thread, or reporter directory. Incoming call UI, mute, camera toggle, and "
            "call history. Reporters can reach editors; teams on an IR case can join a group call. "
            "Built with WebRTC (browser/mobile) and SignalR signaling on the existing .NET API.",
        ),
        (
            "4.15 AI News View (Original &amp; AI Tabs)",
            "<b>Design choice (recommended): inside the article page</b> — not a separate outside page. "
            "When a user opens any published dispatch, two tabs appear at the top: "
            "<b>Original</b> (reporter's exact text and media) and <b>AI View</b> (AI-generated summary, "
            "simplified language, key bullet points, optional Kannada/English/Hindi rewrite). "
            "User taps to switch — same story, same page, no extra navigation. "
            "When admin Inclines a dispatch to publish, the backend calls <b>Google Gemini</b> or "
            "<b>OpenAI GPT</b> (API key configured in admin settings, stored server-side only) to "
            "generate and save the AI version alongside the original. AI output is clearly labelled. "
            "Admin can toggle AI on/off, pick provider, and regenerate from admin portal.",
        ),
    ]
    for title, desc in modules:
        story.append(Paragraph(title, styles["h2"]))
        story.append(Paragraph(desc, styles["body"]))

    story.append(PageBreak())

    # ---- 5. ADMIN PORTAL SCREENS ----
    story.append(Paragraph("5. Editorial Admin Portal — Separate Screen Structure", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Client requirement: dedicated admin website with isolated screens per function "
            "(not embedded in consumer app). Each screen is role-gated.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        make_table(
            styles,
            [
                ["Admin Screen", "Purpose", "Roles"],
                ["Dashboard Overview", "KPIs: users, pending reporters, pending dispatches, earnings, IR count", "All admins"],
                ["Dispatch Review Queue", "Incline / Decline submitted news with media preview", "Sub Admin+"],
                ["Reporter Applications", "Review credentials, Incline or Decline registration", "Admin+"],
                ["Reporter Directory", "Active reporters, status, beat, suspend/reinstate", "Admin+"],
                ["User Management", "Consumers, premium status, role assignment", "Super Admin"],
                ["Advertisement Manager", "CRUD ads, slots, scheduling, city targeting", "Admin+"],
                ["Investigation (IR) Center", "Create IR, assign IO, assign teams, view timeline", "Admin+"],
                ["Team Management", "Create teams, members, assignment history", "Admin+"],
                ["Report Consolidation", "Merge team field reports per IR case", "Admin, IO"],
                ["Analytics & Earnings", "Charts, export, reporter payouts summary", "Admin+"],
                ["System Settings", "Cities, languages, categories, reason codes, notifications", "Super Admin"],
                ["AI Settings", "Gemini/GPT provider, API key, enable AI View, regenerate", "Super Admin"],
                ["Audit Log", "Immutable log of all editorial and admin actions", "Super Admin"],
            ],
            col_widths=[3.5 * cm, CONTENT_WIDTH - 7 * cm, 3.5 * cm],
        )
    )
    story.append(PageBreak())

    # ---- 6. VISUAL UI FLOW DIAGRAMS ----
    story.append(Paragraph("6. Visual User Flow Diagrams", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Below is a <b>simple summary table</b> of all flows, then <b>screen-by-screen pictures</b> for each. "
            "Phone frames = public app. Wider panels = admin website. "
            "Green = <b>Incline</b> (approve). Red = <b>Decline</b> (reject).",
            styles["body"],
        )
    )
    story.append(Spacer(1, 8))
    story.append(Paragraph("6A. All Flows at a Glance (One Line Each)", styles["h2"]))
    story.append(Spacer(1, 4))
    story.append(
        make_table(
            styles,
            get_flow_summary_table(),
            col_widths=[1.2 * cm, 4.2 * cm, CONTENT_WIDTH - 5.4 * cm],
        )
    )
    story.append(Spacer(1, 12))
    story.append(Paragraph("6B. Visual Screen Flows (Step by Step)", styles["h2"]))
    story.append(Spacer(1, 6))

    flow_sections = build_flow_sections(CONTENT_WIDTH)
    for i, section in enumerate(flow_sections):
        story.append(section)
        if i < len(flow_sections) - 1:
            story.append(PageBreak())

    story.append(PageBreak())

    # ---- 6C. FLOW STEP DETAILS ----
    story.append(Paragraph("6C. Flow Step Details (Quick Reference)", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Short step list for each flow — for team reference during development and client walkthrough.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 6))

    flows = [
        (
            "Flow 1 — Consumer (Read News)",
            "A normal person opens the app, picks city and language, reads and watches local news.",
            [
                "Open app → select city (e.g. Bangalore) and language (e.g. Kannada).",
                "Scroll the news feed — stories, photos, videos, and ads.",
                "Tap a story → read full article; switch <b>Original</b> or <b>AI View</b> tabs (see Flow 8).",
                "Endorse (trust it), Discuss (comment), or Circulate (share).",
                "Open Briefs tab → swipe short news videos.",
                "Search any topic, or track an investigation case number.",
                "Note: Premium members can also post news — see Flow 3.",
            ],
        ),
        (
            "Flow 2 — Reporter (Journalist)",
            "A journalist registers, gets approved, receives press ID, posts news after admin check.",
            [
                "Apply as reporter — name, area, languages, ID document.",
                "Wait — status shows Under Review.",
                "Admin Inclines (approves) or Declines (rejects) in admin portal.",
                "On approval → digital press ID card and appointment letter.",
                "Create news with photo, video, or audio attached.",
                "Admin Inclines dispatch → published to city/language feed.",
            ],
        ),
        (
            "Flow 3 — Premium User Posts News",
            "Premium member uploads photo/video news; admin approves before it goes public.",
            [
                "Premium user taps Create / Submit news.",
                "Upload images or video + write what happened.",
                "Status: Pending Editorial Review — not live yet.",
                "Sub Admin does first check.",
                "Admin gives final Incline or Decline.",
                "Incline → story appears in feed with user's name.",
                "Decline → user gets reason and can fix and resubmit.",
            ],
        ),
        (
            "Flow 4 — Editorial Approval (All News)",
            "Every story waits for admin Incline or Decline — true news policy.",
            [
                "Reporter or Premium user submission enters review queue.",
                "Admin previews text, photos, videos, and details.",
                "Click Incline to publish or Decline with reason.",
                "Action saved in audit log permanently.",
                "Author gets notification; published story appears in feed.",
            ],
        ),
        (
            "Flow 5 — Investigation Case (IR)",
            "Admin opens a case with tracking number; public can check status.",
            [
                "Admin creates case — system gives number (e.g. IR-BLR-2026-00042).",
                "Assign investigation officer and field teams.",
                "Teams submit field reports; officer merges them.",
                "Public user enters number on Track page → sees timeline.",
                "Admin closes case when done.",
            ],
        ),
        (
            "Flow 6 — Ads & Premium",
            "Admin runs ads; users upgrade to Premium; reporters see earnings.",
            [
                "Admin creates ad — image/video, city, placement slot.",
                "Ads show in feed and Briefs (clearly labelled).",
                "User upgrades to Premium for ad-free and extra features.",
                "Reporter views earnings — views, endorsements, income.",
                "Admin sees platform-wide analytics and payouts.",
            ],
        ),
        (
            "Flow 7 — Audio & Video Calls",
            "People talk inside the app — audio or video — no WhatsApp needed.",
            [
                "Open a profile → tap Audio Call or Video Call.",
                "Other person gets ring notification.",
                "They accept → live call starts.",
                "Mute, turn camera off, or hang up during call.",
                "IR teams can do group calls for case coordination.",
            ],
        ),
        (
            "Flow 8 — AI News View (Original vs AI)",
            "On the same article page, user switches between real story and AI simple version.",
            [
                "User opens a published news story (inside the app).",
                "Two tabs at top: Original | AI View — on the same page (not separate website).",
                "Original tab → reporter's exact text, photos, and video.",
                "AI View tab → simple summary, bullet points, easy language (or translation).",
                "Label shown: AI-generated via Gemini or GPT.",
                "When admin publishes news, server auto-creates AI version using API key.",
                "Admin sets Gemini or GPT key in AI Settings (key never shown to users).",
            ],
        ),
    ]

    for title, one_line, steps in flows:
        story.append(Paragraph(title, styles["h3"]))
        story.append(
            Paragraph(f"<i><b>In one line:</b> {one_line}</i>", styles["body"])
        )
        for i, step in enumerate(steps, 1):
            story.append(Paragraph(f"<b>{i}.</b> {step}", styles["flow_step"]))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ---- 7. RECOMMENDED IMPROVEMENTS ----
    story.append(Paragraph("7. Recommended Additions (Media House Best Practices)", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Based on industry standards for digital newsrooms, the following enhancements "
            "are recommended beyond the stated client requirements:",
            styles["body"],
        )
    )
    improvements = [
        ("Breaking News Push Alerts", "Editor-triggered push notifications for verified breaking dispatches by city."),
        ("Editor's Pick / Featured Slot", "Curated top story placement on feed — admin-controlled."),
        ("Content Versioning", "Track edits after publication; show 'Updated' timestamp and change summary."),
        ("Tip-off / Whistleblower Channel", "Anonymous tip submission with encrypted handling for investigative desk."),
        ("Press Release Portal", "Separate channel for official government/corporate statements."),
        ("Multi-language CMS", "Admin UI and dispatch content in Kannada, English, Hindi with translation workflow."),
        ("Reporter Beat Map", "Visual map of coverage areas; assign exclusive beats to avoid duplicate reporting."),
        ("Engagement Analytics for Editors", "Heatmaps: which topics, cities, and formats perform best."),
        ("GDPR / Data Privacy Module", "Consent management, data export, account deletion — essential for user trust."),
        ("Two-Factor Auth for Admins", "Mandatory 2FA for all editorial admin accounts."),
        ("Watermark on Field Media", "Automatic PressBangalore watermark on reporter uploads for attribution."),
        ("Live Broadcast", "Live video stream for press conferences and breaking events."),
        ("RSS & Syndication API", "Allow partner sites to syndicate published feeds with attribution."),
        ("AI Original / AI View Tabs", "Inside article page — switch between reporter text and AI summary (Gemini/GPT)."),
        ("Print-Ready Export", "Generate PDF of dispatch for print edition compatibility."),
    ]
    story.append(
        make_table(
            styles,
            [["Enhancement", "Benefit"]] + [[a, b] for a, b in improvements],
            col_widths=[4.5 * cm, CONTENT_WIDTH - 4.5 * cm],
        )
    )
    story.append(PageBreak())

    # ---- 8. TECHNOLOGY & INFRASTRUCTURE ----
    story.append(Paragraph("8. Technology Stack &amp; Infrastructure", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "The chosen stack is suitable for the full platform including news, admin workflows, "
            "and real-time audio/video communication. <b>Render</b> hosts the API and services; "
            "<b>Cloudflare</b> handles CDN, DNS, SSL, and media edge delivery — together this is "
            "enough for production launch at the proposed scale.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        make_table(
            styles,
            [
                ["Layer", "Technology", "Notes"],
                ["Consumer & Reporter UI", "React 19, TypeScript, Vite, Tailwind CSS", "Responsive web + Capacitor Android app"],
                ["Admin Portal", "React (separate deployment)", "Dedicated subdomain e.g. admin.pressbangalore.com"],
                ["API", ".NET 8, HotChocolate GraphQL", "Queries/mutations for all domain operations"],
                ["Real-time / Calls", "SignalR + WebRTC", "Call signaling on API; peer audio/video in app"],
                ["AI Layer", "Google Gemini or OpenAI GPT", "API key on server; generates AI View on publish"],
                ["File Upload", "REST multipart + Cloudflare R2/CDN", "Images, video, audio attachments"],
                ["Database", "PostgreSQL (managed)", "Full relational schema with audit tables"],
                ["Auth", "JWT + role-based access control", "BCrypt passwords; 2FA for admins (recommended)"],
                ["Hosting — API", "Render", ".NET API service, SignalR WebSockets, background jobs"],
                ["Hosting — Frontend", "Cloudflare Pages / CDN", "Static web app, fast global delivery"],
                ["DNS & Security", "Cloudflare", "SSL, DDoS protection, caching, optional R2 storage"],
                ["Mobile", "Capacitor 8 (Android)", "Same codebase as web; APK + installable PWA"],
            ],
            col_widths=[3.5 * cm, 4.8 * cm, CONTENT_WIDTH - 8.3 * cm],
        )
    )
    story.append(Spacer(1, 10))
    story.append(Paragraph("8.1 Audio &amp; Video Calls — Technology Fit", styles["h2"]))
    story += bullet_list(
        [
            "<b>Signaling</b> — ASP.NET Core SignalR on Render manages call setup, ring, accept, decline, and hang-up.",
            "<b>Media</b> — WebRTC in React (web) and Capacitor (Android) handles live audio and video streams peer-to-peer.",
            "<b>STUN/TURN</b> — Cloudflare (or a lightweight TURN add-on) ensures calls work across mobile networks and firewalls.",
            "<b>Render + Cloudflare is sufficient</b> — no separate heavy media server required for standard 1-to-1 and small group calls.",
            "Call features integrate with existing user roles: consumers, reporters, editors, and IR teams can call permitted contacts.",
        ],
        styles["bullet"],
    )
    story.append(Spacer(1, 8))
    story.append(Paragraph("8.2 AI News View — Design &amp; Technology", styles["h2"]))
    story.append(
        Paragraph(
            "<b>Where to put it:</b> Inside the app, on the <b>same article detail page</b> — not a separate "
            "outside website. Two tabs (<i>Original</i> | <i>AI View</i>) sit below the headline. "
            "This is the best UX: user stays on one story, taps to compare real vs simplified version.",
            styles["body"],
        )
    )
    story += bullet_list(
        [
            "<b>Original tab</b> — exact published dispatch from reporter or Premium user (text, images, video).",
            "<b>AI View tab</b> — generated summary, bullet key points, plain language, optional language rewrite.",
            "<b>Provider</b> — Google Gemini API or OpenAI GPT API; admin chooses one in AI Settings.",
            "<b>API key</b> — stored only on Render server (environment variable); never exposed to mobile/browser.",
            "<b>When generated</b> — automatically when admin Inclines (publishes) a dispatch; cached in database.",
            "<b>Label</b> — AI View always shows “AI-generated” badge so readers know it is not the original report.",
            "<b>Admin controls</b> — enable/disable AI, switch provider, regenerate AI text for a story.",
        ],
        styles["bullet"],
    )
    story.append(PageBreak())

    # ---- 9. DEVELOPMENT PHASES ----
    story.append(Paragraph("9. Development Phases & Deliverables", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    phases = [
        (
            "Phase 0 — Demo (Completed)",
            "UI demo with mock data; Android APK; all hero journeys navigable; client presentation ready.",
        ),
        (
            "Phase 1 — Production Foundation",
            "Backend integration; real auth and file upload; separate admin portal; Incline/Decline workflow; "
            "reporter registration and dispatch queues; news feed with filters; IR module; basic ads; "
            "audio/video call signaling and 1-to-1 calls; AI View (Gemini/GPT) on publish.",
        ),
        (
            "Phase 2 — Growth & Monetization",
            "Premium subscriptions; payment gateway; push notifications; PDF ID cards and appointment letters; "
            "earnings dashboard; analytics; email/SMS notifications; group audio/video calls.",
        ),
        (
            "Phase 3 — Advanced Media",
            "Live broadcast; advertiser self-serve; syndication API; multi-language CMS; tip-off channel; "
            "advanced ad targeting and billing.",
        ),
    ]
    for title, desc in phases:
        story.append(Paragraph(title, styles["h2"]))
        story.append(Paragraph(desc, styles["body"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("9.1 What Will Be Developed — Summary Checklist", styles["h2"]))
    checklist = [
        "Public news feed (location + language filters)",
        "News dispatch with image, video, audio attachments",
        "Briefs (reels) — short vertical video feed",
        "Reporter registration, Incline/Decline approval, status tracking",
        "Digital reporter ID card and appointment letter (PDF)",
        "In-app audio/video field recording for reporters",
        "User and Premium user accounts with profile dashboard",
        "Premium user upload news (photo/video) with editorial approval",
        "Editorial Incline/Decline approval for all submitted content",
        "Separate admin portal with dedicated screens per function",
        "Super Admin / Admin / Sub Admin role hierarchy",
        "Advertisement panel with feed and Briefs placements",
        "IR investigations with trackable number and public tracker",
        "IO assignment and multi-team report consolidation",
        "Professional terminology (Endorse, Discuss, Incline, Decline)",
        "True news policy with source attribution and audit trail",
        "Search, analytics, earnings information",
        "In-app audio and video calls (user-to-user, reporter-to-editor, team calls)",
        "AI View tab on article page (Original vs AI summary — Gemini or GPT)",
        "Web application + Android mobile app (single codebase)",
    ]
    story += bullet_list(checklist, styles["bullet"])

    story.append(PageBreak())

    # ---- 10. SYSTEM ARCHITECTURE (VISUAL) ----
    story.append(Paragraph("10. High-Level System Architecture", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Three portals connect through a single API layer to PostgreSQL. "
            "All submitted content follows the publish path at the bottom.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 8))
    story.append(SystemArchitectureDiagram(CONTENT_WIDTH))

    story.append(Spacer(1, 16))
    story.append(Paragraph("11. Conclusion", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "The PressBangalore demo validates the user experience and core journeys discussed with the client. "
            "This document defines the full production scope: a three-portal architecture with professional "
            "editorial language, mandatory content review for true news integrity, separate admin screens, "
            "in-app audio and video communication, and comprehensive modules for reporters, investigations, "
            "advertisements, and analytics. The React + .NET + PostgreSQL stack on Render and Cloudflare "
            "is well suited for web, mobile, and real-time calls.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 16))
    story.append(Paragraph("12. Project Budget", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))
    story.append(
        make_table(
            styles,
            [
                ["Item", "Details"],
                ["Total project cost", "₹3,00,000 (Rupees Three Lakhs Only)"],
                [
                    "Deliverables included",
                    "Public web application · Android mobile app · Reporter portal · "
                    "Editorial admin portal · Backend API · News feed, Briefs, approvals, IR module, "
                    "advertisements, analytics, audio & video calls, AI Original/AI View tabs",
                ],
                [
                    "Hosting (client / operational)",
                    "Render (API + services) · Cloudflare (CDN, DNS, SSL, media edge) — "
                    "sufficient for launch; hosting costs billed separately to client infra accounts",
                ],
                ["Demo status", "UI demo completed — production build per scope above"],
            ],
            col_widths=[4 * cm, CONTENT_WIDTH - 4 * cm],
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "<b>Note:</b> Budget covers design, development, testing, and deployment setup for web and "
            "mobile as described in this document. Third-party paid services (SMS gateway, payment gateway, "
            "domain registration, Render/Cloudflare usage beyond free tiers, and Gemini/GPT API usage charges) "
            "are excluded unless agreed separately.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "<i>Document prepared by Haja Mainudeen, Full Stack Developer (7 years experience). "
            "For questions or scope adjustments, please contact directly.</i>",
            styles["body"],
        )
    )

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    build_document()
