"""
Generate AP Media Development Quotation (brief PDF)
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path(__file__).parent / "AP-Media-Quotation.pdf"
CONTENT_WIDTH = A4[0] - 4 * cm

PRIMARY = colors.HexColor("#1a365d")
ACCENT = colors.HexColor("#c53030")
MUTED = colors.HexColor("#4a5568")
LIGHT_BG = colors.HexColor("#edf2f7")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontSize=22,
            leading=28,
            textColor=PRIMARY,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontSize=12,
            leading=16,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontSize=9,
            leading=13,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=3,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontSize=13,
            leading=18,
            textColor=PRIMARY,
            spaceBefore=14,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=9.5,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontSize=9.5,
            leading=13,
            leftIndent=12,
            spaceAfter=2,
        ),
        "total": ParagraphStyle(
            "Total",
            parent=base["Normal"],
            fontSize=12,
            leading=16,
            textColor=ACCENT,
            fontName="Helvetica-Bold",
            alignment=TA_RIGHT,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    }


def make_table(data, col_widths, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ]
    t.setStyle(TableStyle(style))
    return t


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0] / 2, 12 * mm, f"AP Media Quotation  |  Page {doc.page}")
    canvas.restoreState()


def build():
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=2 * cm,
        title="AP Media Development Quotation",
        author="Haja Mainudeen",
    )
    story = []

    # Cover header
    story.append(Paragraph("AP Media", styles["title"]))
    story.append(Paragraph("Development Quotation", styles["subtitle"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("<b>Date:</b> 25 June 2026 &nbsp;|&nbsp; <b>Valid until:</b> 25 July 2026", styles["meta"]))
    story.append(Paragraph("<b>Prepared for:</b> FG Media Group", styles["meta"]))
    story.append(Paragraph("<b>Prepared by:</b> Haja Mainudeen — Full Stack Developer", styles["meta"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("1. Project Overview", styles["h1"]))
    story.append(
        Paragraph(
            "AP Media is a verified news and media platform built around trust, fact-based content, "
            "and editorial control. A working UI demo has been delivered. This quotation covers full-stack "
            "production development as agreed in the 24 June 2026 meeting — to be completed within one month.",
            styles["body"],
        )
    )

    story.append(Paragraph("2. Scope Summary", styles["h1"]))
    scope_items = [
        "News feed with breaking news, scenes, and user posts (photo, video, audio, documents)",
        "User profiles, roles, subscriptions, followers, and trust indicators",
        "Admin verification before publish; counter-statements and evidence support",
        "Reporter registration, approval workflow, and digital ID card",
        "Investigation requests (IR numbers, regional routing, IO assignment, public tracker)",
        "Engagement: like, dislike, comment, endorse, circulate, sponsor, save",
        "In-app chat; wallet for e-papers, sponsorship, and investigation fees",
        "E-paper subscriptions, live TV channels, RSS feeds, publisher dashboard",
        "Hub: marketplace, jobs, courses, events, and community groups",
        "Trust & fact scoring framework with AI integration points",
        "Vira AI avatar — architecture and consent-based integration framework",
        "CCTV / surveillance hooks for evidence storage",
        "React web + Python API + scalable PostgreSQL database",
    ]
    for item in scope_items:
        story.append(Paragraph(f"&bull; {item}", styles["bullet"]))

    story.append(Paragraph("3. Technology & Timeline", styles["h1"]))
    story.append(
        make_table(
            [
                ["Layer", "Technology"],
                ["Web", "React (client UI code & design specs)"],
                ["Backend", "Python APIs"],
                ["Database", "PostgreSQL — scalable schema (Week 1 approval)"],
                ["AI", "Gemini & GPT-4 (client API keys)"],
                ["Mobile", "Flutter 4 — Phase 2 (web-first in Month 1)"],
            ],
            [4.5 * cm, CONTENT_WIDTH - 4.5 * cm],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        make_table(
            [
                ["Milestone", "Target"],
                ["DB architecture submitted", "Week 1"],
                ["Backend + core modules", "Weeks 1–3"],
                ["Real-time data demo", "Before next review meeting"],
                ["Full delivery", "4 weeks (1 month)"],
            ],
            [6 * cm, CONTENT_WIDTH - 6 * cm],
        )
    )

    story.append(Paragraph("4. Investment — Phase 1 (Month 1)", styles["h1"]))
    story.append(
        make_table(
            [
                ["Component", "Amount (INR)"],
                ["React web application & UI integration", "₹60,000"],
                ["Python backend API & business logic", "₹70,000"],
                ["Database design, migrations & seed data", "₹25,000"],
                ["Reporter, admin & investigation modules", "₹45,000"],
                ["Wallet, e-paper, live TV & hub foundations", "₹30,000"],
                ["Trust score & content verification flow", "₹20,000"],
                ["Total", "₹2,50,000"],
            ],
            [10.5 * cm, CONTENT_WIDTH - 10.5 * cm],
        )
    )
    story.append(Paragraph("<b>₹2,50,000</b> — Rupees Two Lakhs Fifty Thousand Only", styles["total"]))

    story.append(Paragraph("5. Phase 2 — Advanced Modules (Indicative)", styles["h1"]))
    story.append(
        make_table(
            [
                ["Module", "Indicative (INR)"],
                ["Vira AI clone (voice, chat, debate, Zoom/Meet/Teams)", "₹1,20,000"],
                ["Flutter 4 mobile app (Android + iOS)", "₹80,000"],
                ["CCTV / surveillance network integration", "₹50,000"],
                ["AI newsroom & advanced analytics", "₹40,000"],
                ["Payment gateway, notifications, production hardening", "₹35,000"],
            ],
            [10.5 * cm, CONTENT_WIDTH - 10.5 * cm],
        )
    )
    story.append(
        Paragraph(
            "<i>Phase 2 quoted separately upon Phase 1 sign-off.</i>",
            styles["body"],
        )
    )

    story.append(Paragraph("6. Payment Terms", styles["h1"]))
    story.append(
        make_table(
            [
                ["Installment", "Trigger", "Amount"],
                ["1st", "Kick-off & DB architecture approval", "₹75,000 (30%)"],
                ["2nd", "Backend + admin modules complete", "₹87,500 (35%)"],
                ["3rd", "Demo delivery & acceptance", "₹87,500 (35%)"],
            ],
            [2.5 * cm, 7.5 * cm, CONTENT_WIDTH - 10 * cm],
        )
    )

    story.append(Paragraph("7. Included / Excluded", styles["h1"]))
    story.append(Paragraph("<b>Included:</b> development, testing, deployment setup guidance, weekly updates, source code handover, 30-day critical bug-fix support.", styles["body"]))
    story.append(
        Paragraph(
            "<b>Excluded:</b> hosting charges, third-party API costs (Gemini/GPT/SMS/payments), domain, content/legal advisory, physical ID printing, Phase 2 unless agreed.",
            styles["body"],
        )
    )

    story.append(Paragraph("8. Client Responsibilities", styles["h1"]))
    for item in [
        "Share complete UI code and design specifications",
        "Provide Gemini and GPT-4 API keys",
        "Approve database architecture within Week 1",
        "Timely feedback on demos and module reviews",
    ]:
        story.append(Paragraph(f"&bull; {item}", styles["bullet"]))

    story.append(Spacer(1, 0.6 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
    story.append(Spacer(1, 0.4 * cm))
    story.append(
        make_table(
            [
                ["Developer", "Haja Mainudeen — mainudeen369@gmail.com"],
                ["Client", "FG Media Group — Signature / Date: _______________"],
            ],
            [3.5 * cm, CONTENT_WIDTH - 3.5 * cm],
            header=False,
        )
    )
    story.append(Spacer(1, 0.4 * cm))
    story.append(
        Paragraph(
            "<i>Based on 24 June 2026 meeting decisions and delivered demo. Scope changes priced separately.</i>",
            styles["footer"],
        )
    )

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    build()
