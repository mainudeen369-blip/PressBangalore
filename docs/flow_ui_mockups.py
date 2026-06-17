"""
Compact UI screen mockups for PressBangalore flow diagrams (ReportLab).
"""
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Flowable

# Brand palette
PRIMARY = colors.HexColor("#1a365d")
ACCENT = colors.HexColor("#c53030")
SUCCESS = colors.HexColor("#276749")
WARNING = colors.HexColor("#c05621")
MUTED = colors.HexColor("#718096")
LIGHT_BG = colors.HexColor("#f7fafc")
CARD_BORDER = colors.HexColor("#e2e8f0")
WHITE = colors.white
SCREEN_BG = colors.HexColor("#ffffff")
ADMIN_SIDEBAR = colors.HexColor("#2d3748")


def _wrap_lines(canvas, text, font, size, max_width):
    measure = (
        (lambda t, f, s: canvas.stringWidth(t, f, s))
        if canvas is not None
        else (lambda t, f, s: stringWidth(t, f, s))
    )
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if measure(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def _banner_height(title_lines, subtitle_lines):
    """Compute banner height from wrapped line counts."""
    top_pad = 5 * mm
    bottom_pad = 4 * mm
    title_leading = 5.2 * mm
    subtitle_leading = 4.2 * mm
    gap = 2 * mm
    return (
        top_pad
        + len(title_lines) * title_leading
        + gap
        + len(subtitle_lines) * subtitle_leading
        + bottom_pad
    )


class FlowIntroBanner(Flowable):
    """Section header with title + subtitle on separate lines."""

    def __init__(self, title, subtitle, width):
        Flowable.__init__(self)
        self.title = title
        self.subtitle = subtitle
        self.width = width
        self.pad_left = 10 * mm
        self.text_width = width - self.pad_left - 5 * mm
        self.title_lines = _wrap_lines(None, title, "Helvetica-Bold", 11, self.text_width)[:2]
        self.subtitle_lines = _wrap_lines(None, subtitle, "Helvetica", 8, self.text_width)[:2]
        self.height = _banner_height(self.title_lines, self.subtitle_lines)

    def draw(self):
        c = self.canv
        c.setFillColor(PRIMARY)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(0, 0, 4 * mm, self.height, fill=1, stroke=0)

        x = self.pad_left
        y = self.height - 5 * mm

        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 11)
        for line in self.title_lines:
            c.drawString(x, y, line)
            y -= 5.2 * mm

        y -= 2 * mm

        c.setFillColor(colors.HexColor("#bee3f8"))
        c.setFont("Helvetica", 8)
        for line in self.subtitle_lines:
            c.drawString(x, y, line)
            y -= 4.2 * mm


class PhoneScreen(Flowable):
    """Single compact mobile UI mockup."""

    def __init__(self, step, screen_title, elements, caption, width=4.1 * cm):
        Flowable.__init__(self)
        self.step = step
        self.screen_title = screen_title
        self.elements = elements
        self.caption = caption
        self.phone_w = width
        self.phone_h = 6.8 * cm
        self.height = self.phone_h + 1.15 * cm
        self.width = width

    def _draw_element(self, c, el, x, y, inner_w):
        t = el.get("type")
        if t == "chips":
            cx = x
            for chip in el.get("items", []):
                tw = c.stringWidth(chip, "Helvetica", 5.5) + 8
                c.setFillColor(colors.HexColor("#ebf8ff"))
                c.setStrokeColor(colors.HexColor("#90cdf4"))
                c.roundRect(cx, y - 7, tw, 8, 3, fill=1, stroke=1)
                c.setFillColor(PRIMARY)
                c.setFont("Helvetica", 5.5)
                c.drawString(cx + 4, y - 4.5, chip)
                cx += tw + 4
            return y - 12
        if t == "stories":
            cx = x
            for label in el.get("items", [])[:5]:
                c.setFillColor(ACCENT)
                c.circle(cx + 5, y - 5, 5, fill=1, stroke=0)
                c.setFillColor(MUTED)
                c.setFont("Helvetica", 4.5)
                c.drawCentredString(cx + 5, y - 14, label[:6])
                cx += 14
            return y - 18
        if t == "card":
            h = 22 + 9 * len(el.get("lines", [])[:2])
            c.setFillColor(LIGHT_BG)
            c.setStrokeColor(CARD_BORDER)
            c.roundRect(x, y - h, inner_w, h, 4, fill=1, stroke=1)
            c.setFillColor(PRIMARY)
            c.setFont("Helvetica-Bold", 6)
            c.drawString(x + 5, y - 9, el.get("title", "")[:28])
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 5.5)
            ly = y - 16
            for line in el.get("lines", [])[:2]:
                for wl in _wrap_lines(c, line, "Helvetica", 5.5, inner_w - 10)[:1]:
                    c.drawString(x + 5, ly, wl[:40])
                    ly -= 7
            if el.get("badge"):
                c.setFillColor(SUCCESS if el["badge"] == "Verified" else WARNING)
                c.roundRect(x + inner_w - 28, y - h + 4, 24, 8, 2, fill=1, stroke=0)
                c.setFillColor(WHITE)
                c.setFont("Helvetica-Bold", 5)
                c.drawCentredString(x + inner_w - 16, y - h + 7, el["badge"][:8])
            return y - h - 5
        if t == "media":
            c.setFillColor(colors.HexColor("#2d3748"))
            c.roundRect(x, y - 28, inner_w, 28, 4, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(x + inner_w / 2, y - 18, el.get("icon", "▶"))
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 5)
            c.drawCentredString(x + inner_w / 2, y - 32, el.get("label", "Video")[:20])
            return y - 38
        if t == "actions":
            bw = (inner_w - 6) / 2
            for i, (label, color) in enumerate(el.get("buttons", [])[:2]):
                bx = x + i * (bw + 6)
                c.setFillColor(color)
                c.roundRect(bx, y - 12, bw, 12, 3, fill=1, stroke=0)
                c.setFillColor(WHITE)
                c.setFont("Helvetica-Bold", 6)
                c.drawCentredString(bx + bw / 2, y - 8, label)
            return y - 18
        if t == "status":
            c.setFillColor(colors.HexColor(el.get("bg", "#fefcbf")))
            c.roundRect(x, y - 12, inner_w, 12, 3, fill=1, stroke=0)
            c.setFillColor(colors.HexColor(el.get("color", "#975a16")))
            c.setFont("Helvetica-Bold", 6)
            c.drawCentredString(x + inner_w / 2, y - 8, el.get("text", ""))
            return y - 18
        if t == "field":
            c.setStrokeColor(CARD_BORDER)
            c.setFillColor(WHITE)
            c.roundRect(x, y - 10, inner_w, 10, 2, fill=1, stroke=1)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 5.5)
            c.drawString(x + 4, y - 7, el.get("placeholder", "")[:30])
            return y - 14
        if t == "nav":
            c.setFillColor(PRIMARY)
            c.rect(x, y - 10, inner_w, 10, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica", 5)
            items = el.get("items", [])
            spacing = inner_w / max(len(items), 1)
            for i, item in enumerate(items):
                c.drawCentredString(x + spacing * i + spacing / 2, y - 7, item[:8])
            return y - 14
        if t == "tabs":
            items = el.get("items", ["Original", "AI View"])
            active = el.get("active", 0)
            tw = inner_w / max(len(items), 1)
            for i, label in enumerate(items[:3]):
                tx = x + i * tw
                is_active = i == active
                c.setFillColor(PRIMARY if is_active else LIGHT_BG)
                c.setStrokeColor(CARD_BORDER)
                c.roundRect(tx + 1, y - 11, tw - 2, 11, 3, fill=1, stroke=1)
                c.setFillColor(WHITE if is_active else MUTED)
                c.setFont("Helvetica-Bold" if is_active else "Helvetica", 5.5)
                c.drawCentredString(tx + tw / 2, y - 7.5, label[:12])
            return y - 15
        if t == "stat_row":
            sw = inner_w / 3
            for i, (val, lbl) in enumerate(el.get("items", [])[:3]):
                c.setFillColor(LIGHT_BG)
                c.roundRect(x + i * sw, y - 16, sw - 2, 16, 2, fill=1, stroke=0)
                c.setFillColor(PRIMARY)
                c.setFont("Helvetica-Bold", 7)
                c.drawCentredString(x + i * sw + sw / 2 - 1, y - 8, val)
                c.setFillColor(MUTED)
                c.setFont("Helvetica", 4.5)
                c.drawCentredString(x + i * sw + sw / 2 - 1, y - 14, lbl)
            return y - 20
        if t == "timeline":
            for item in el.get("items", [])[:4]:
                c.setFillColor(SUCCESS if item.get("done") else CARD_BORDER)
                c.circle(x + 4, y - 4, 2.5, fill=1, stroke=0)
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 5.5)
                c.drawString(x + 10, y - 6, item.get("text", "")[:24])
                y -= 9
            return y - 4
        return y

    def draw(self):
        c = self.canv
        px, py = 0, 1.15 * cm

        # Step badge
        c.setFillColor(ACCENT)
        c.circle(px + 5 * mm, py + self.phone_h + 3 * mm, 4 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(px + 5 * mm, py + self.phone_h + 1.5 * mm, str(self.step))

        # Phone frame
        c.setFillColor(colors.HexColor("#1a202c"))
        c.roundRect(px - 1, py - 1, self.phone_w + 2, self.phone_h + 2, 8, fill=1, stroke=0)
        c.setFillColor(SCREEN_BG)
        c.roundRect(px, py, self.phone_w, self.phone_h, 7, fill=1, stroke=0)

        # Status bar
        c.setFillColor(PRIMARY)
        c.roundRect(px, py + self.phone_h - 9 * mm, self.phone_w, 9 * mm, 0, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawString(px + 4, py + self.phone_h - 6.5 * mm, self.screen_title[:18])

        # Content area
        inner_x = px + 4
        inner_w = self.phone_w - 8
        cy = py + self.phone_h - 12 * mm
        for el in self.elements:
            cy = self._draw_element(c, el, inner_x, cy, inner_w)

        # Caption
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.5)
        for i, line in enumerate(_wrap_lines(c, self.caption, "Helvetica", 6.5, self.phone_w)[:2]):
            c.drawCentredString(px + self.phone_w / 2, py - 5 * mm - i * 8, line)


class AdminScreen(Flowable):
    """Compact desktop admin panel mockup."""

    def __init__(self, step, screen_title, sidebar, elements, caption, width=5.6 * cm):
        Flowable.__init__(self)
        self.step = step
        self.screen_title = screen_title
        self.sidebar = sidebar
        self.elements = elements
        self.caption = caption
        self.panel_w = width
        self.panel_h = 5.2 * cm
        self.height = self.panel_h + 1.15 * cm
        self.width = width

    def draw(self):
        c = self.canv
        px, py = 0, 1.15 * cm

        c.setFillColor(ACCENT)
        c.circle(px + 5 * mm, py + self.panel_h + 3 * mm, 4 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(px + 5 * mm, py + self.panel_h + 1.5 * mm, str(self.step))

        c.setStrokeColor(CARD_BORDER)
        c.setFillColor(WHITE)
        c.roundRect(px, py, self.panel_w, self.panel_h, 5, fill=1, stroke=1)

        # Sidebar
        sw = 1.6 * cm
        c.setFillColor(ADMIN_SIDEBAR)
        c.roundRect(px, py, sw, self.panel_h, 5, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#a0aec0"))
        c.setFont("Helvetica", 4.5)
        sy = py + self.panel_h - 8
        for item in self.sidebar[:6]:
            c.drawString(px + 4, sy, item[:10])
            sy -= 7

        # Main
        mx = px + sw + 5
        mw = self.panel_w - sw - 10
        c.setFillColor(PRIMARY)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(mx, py + self.panel_h - 10, self.screen_title[:24])
        cy = py + self.panel_h - 18
        for el in self.elements:
            t = el.get("type")
            if t == "field":
                c.setStrokeColor(CARD_BORDER)
                c.setFillColor(WHITE)
                c.roundRect(mx, cy - 10, mw, 10, 2, fill=1, stroke=1)
                c.setFillColor(MUTED)
                c.setFont("Helvetica", 5.5)
                c.drawString(mx + 4, cy - 7, el.get("placeholder", "")[:34])
                cy -= 14
            elif t == "card":
                h = 18
                c.setFillColor(LIGHT_BG)
                c.roundRect(mx, cy - h, mw, h, 3, fill=1, stroke=0)
                c.setFillColor(PRIMARY)
                c.setFont("Helvetica-Bold", 6)
                c.drawString(mx + 4, cy - 8, el.get("title", "")[:28])
                c.setFillColor(MUTED)
                c.setFont("Helvetica", 5)
                c.drawString(mx + 4, cy - 14, el.get("lines", [""])[0][:36])
                cy -= h + 4
            elif t == "status":
                c.setFillColor(colors.HexColor(el.get("bg", "#c6f6d5")))
                c.roundRect(mx, cy - 12, mw, 12, 3, fill=1, stroke=0)
                c.setFillColor(colors.HexColor(el.get("color", "#276749")))
                c.setFont("Helvetica-Bold", 6)
                c.drawCentredString(mx + mw / 2, cy - 8, el.get("text", ""))
                cy -= 16
            elif t == "queue_item":
                c.setFillColor(LIGHT_BG)
                c.roundRect(mx, cy - 14, mw, 14, 3, fill=1, stroke=0)
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 5.5)
                c.drawString(mx + 4, cy - 6, el.get("title", "")[:32])
                c.setFillColor(MUTED)
                c.setFont("Helvetica", 5)
                c.drawString(mx + 4, cy - 11, el.get("meta", "")[:36])
                bx = mx + mw - 34
                for label, col in el.get("buttons", [("Incline", SUCCESS), ("Decline", ACCENT)]):
                    c.setFillColor(col)
                    c.roundRect(bx, cy - 12, 15, 9, 2, fill=1, stroke=0)
                    c.setFillColor(WHITE)
                    c.setFont("Helvetica-Bold", 4.5)
                    c.drawCentredString(bx + 7.5, cy - 8, label[:3])
                    bx += 17
                cy -= 18
            elif t == "kpi":
                kw = mw / 3
                for i, (val, lbl) in enumerate(el.get("items", [])[:3]):
                    c.setFillColor(LIGHT_BG)
                    c.roundRect(mx + i * kw, cy - 16, kw - 3, 16, 2, fill=1, stroke=0)
                    c.setFillColor(ACCENT)
                    c.setFont("Helvetica-Bold", 8)
                    c.drawCentredString(mx + i * kw + kw / 2 - 1.5, cy - 8, val)
                    c.setFillColor(MUTED)
                    c.setFont("Helvetica", 4.5)
                    c.drawCentredString(mx + i * kw + kw / 2 - 1.5, cy - 14, lbl)
                cy -= 20
            elif t == "timeline":
                for item in el.get("items", [])[:3]:
                    c.setFillColor(SUCCESS if item.get("done") else CARD_BORDER)
                    c.circle(mx + 4, cy - 4, 3, fill=1, stroke=0)
                    c.setFillColor(colors.black)
                    c.setFont("Helvetica", 5.5)
                    c.drawString(mx + 12, cy - 6, item.get("text", "")[:30])
                    cy -= 10
                cy -= 4

        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.5)
        for i, line in enumerate(_wrap_lines(c, self.caption, "Helvetica", 6.5, self.panel_w)[:2]):
            c.drawCentredString(px + self.panel_w / 2, py - 5 * mm - i * 8, line)


class FlowRow(Flowable):
    """Horizontal row of screens with arrows."""

    def __init__(self, screens, gap=0.4 * cm, max_width=None):
        Flowable.__init__(self)
        self.screens = screens
        self.gap = gap
        self.arrow_w = 0.4 * cm
        raw_width = sum(s.width for s in screens) + self.arrow_w * (len(screens) - 1) + self.gap * (len(screens) - 1)
        self.scale = 1.0
        if max_width and raw_width > max_width:
            self.scale = max_width / raw_width
        self.width = raw_width * self.scale
        self.height = max(s.height for s in screens) * self.scale

    def draw(self):
        c = self.canv
        x = 0
        for i, screen in enumerate(self.screens):
            c.saveState()
            c.translate(x, 0)
            c.scale(self.scale, self.scale)
            screen.canv = c
            screen.draw()
            c.restoreState()
            x += (screen.width + self.gap) * self.scale
            if i < len(self.screens) - 1:
                mid_y = self.height / 2 + 0.35 * cm
                c.setFillColor(ACCENT)
                c.setFont("Helvetica-Bold", 11)
                c.drawCentredString(x + (self.arrow_w * self.scale) / 2, mid_y, "→")
                x += self.arrow_w * self.scale


class FlowOneLiner(Flowable):
    """Plain-language one-line summary shown below each flow banner."""

    def __init__(self, text, width):
        Flowable.__init__(self)
        self.text = text
        self.width = width
        self.pad = 5 * mm
        lines = _wrap_lines(None, text, "Helvetica", 8.5, width - self.pad * 2)
        self.line_count = min(len(lines), 2)
        self.height = (0.55 + self.line_count * 0.42) * cm

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor("#fffaf0"))
        c.setStrokeColor(colors.HexColor("#dd6b20"))
        c.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=1)
        c.setFillColor(colors.HexColor("#9c4221"))
        c.setFont("Helvetica-Bold", 8)
        c.drawString(self.pad, self.height - 4.5 * mm, "In simple words:")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 8.5)
        max_w = self.width - self.pad * 2
        lines = _wrap_lines(c, self.text, "Helvetica", 8.5, max_w)[:2]
        y = self.height - 9 * mm if len(lines) == 1 else self.height - 7.5 * mm
        for line in lines:
            c.drawString(self.pad, y, line)
            y -= 4 * mm


class FlowSection(Flowable):
    """Complete flow: banner + one-liner + one or two rows of screens."""

    def __init__(self, title, subtitle, one_liner, rows, content_width):
        Flowable.__init__(self)
        self.banner = FlowIntroBanner(title, subtitle, content_width)
        self.one_liner = FlowOneLiner(one_liner, content_width)
        self.rows = [FlowRow(row, max_width=content_width) for row in rows]
        self.width = content_width
        self.height = (
            self.banner.height
            + 0.2 * cm
            + self.one_liner.height
            + 0.25 * cm
            + sum(r.height for r in self.rows)
            + 0.25 * cm * len(self.rows)
        )

    def draw(self):
        c = self.canv
        y = self.height
        c.saveState()
        c.translate(0, y - self.banner.height)
        self.banner.canv = c
        self.banner.draw()
        c.restoreState()
        y -= self.banner.height + 0.2 * cm
        c.saveState()
        c.translate(0, y - self.one_liner.height)
        self.one_liner.canv = c
        self.one_liner.draw()
        c.restoreState()
        y -= self.one_liner.height + 0.25 * cm
        for row in self.rows:
            y -= row.height
            c.saveState()
            c.translate(0, y)
            row.canv = c
            row.draw()
            c.restoreState()
            y -= 0.25 * cm


def _phone(step, title, elements, caption):
    return PhoneScreen(step, title, elements, caption)


def _admin(step, title, sidebar, elements, caption):
    return AdminScreen(step, title, sidebar, elements, caption)


# ─── Flow definitions ─────────────────────────────────────────────────────────

FLOW_DEFINITIONS = [
    {
        "title": "Flow 1 — Consumer Journey (Read & Engage)",
        "subtitle": "Public app  ·  Read news  ·  Watch Briefs  ·  Search  ·  Track cases",
        "one_liner": (
            "A normal person opens the app, picks city and language, reads and watches local news, "
            "and can share opinions — Premium members can also submit news (see Flow 3)."
        ),
        "rows": [
            [
                _phone(1, "Home", [
                    {"type": "chips", "items": ["Bangalore", "Kannada"]},
                    {"type": "stories", "items": ["Live", "City", "Sport", "Biz"]},
                    {"type": "card", "title": "Metro expansion approved", "lines": ["Breaking · Koramangala corridor", "Verified source · 2h ago"], "badge": "Verified"},
                ], "Open app & pick city + language"),
                _phone(2, "Feed", [
                    {"type": "card", "title": "Civic protest peaceful", "lines": ["Town Hall · Photo dispatch", "Endorse · Discuss · Circulate"]},
                    {"type": "card", "title": "Sponsored", "lines": ["Local business spotlight"]},
                ], "Scroll location-filtered news feed"),
                _phone(3, "Article", [
                    {"type": "media", "icon": "▶", "label": "Field video attached"},
                    {"type": "card", "title": "Full dispatch", "lines": ["Audio clip · Source cited", "Fact-check: Verified"]},
                    {"type": "actions", "buttons": [("Endorse", PRIMARY), ("Discuss", MUTED)]},
                ], "Read dispatch with media playback"),
            ],
            [
                _phone(4, "Briefs", [
                    {"type": "media", "icon": "▶", "label": "Vertical field clip"},
                    {"type": "actions", "buttons": [("Endorse", PRIMARY), ("Circulate", ACCENT)]},
                    {"type": "nav", "items": ["Home", "Briefs", "Search", "Profile"]},
                ], "Swipe short video Briefs tab"),
                _phone(5, "Search", [
                    {"type": "field", "placeholder": "Search dispatches, topics..."},
                    {"type": "card", "title": "Trending: Traffic", "lines": ["#SilkBoard #Monsoon"]},
                    {"type": "card", "title": "Track IR case", "lines": ["Enter IR-BLR-2026-..."]},
                ], "Search topics or open IR tracker"),
                _phone(6, "Track IR", [
                    {"type": "field", "placeholder": "IR-BLR-2026-00042"},
                    {"type": "status", "text": "Status: In Progress", "bg": "#ebf8ff", "color": "#2b6cb0"},
                    {"type": "card", "title": "Timeline", "lines": ["Assigned → Field work → Review"]},
                ], "Public investigation status view"),
            ],
        ],
    },
    {
        "title": "Flow 2 — Reporter Journey (Register → Publish)",
        "subtitle": "Apply  ·  Admin approval  ·  Press ID  ·  Post news  ·  Admin checks again",
        "one_liner": (
            "A journalist registers, admin approves, they get a press ID card, "
            "then every news they post is checked by admin before it goes public."
        ),
        "rows": [
            [
                _phone(1, "Register", [
                    {"type": "field", "placeholder": "Name · Beat · Languages"},
                    {"type": "field", "placeholder": "Upload ID document"},
                    {"type": "actions", "buttons": [("Apply", ACCENT), ("Cancel", MUTED)]},
                ], "Submit reporter application"),
                _phone(2, "Status", [
                    {"type": "status", "text": "● Under Review", "bg": "#fefcbf", "color": "#975a16"},
                    {"type": "card", "title": "Application received", "lines": ["Awaiting editorial review", "Notification sent"]},
                ], "Pending until admin decision"),
                _admin(3, "Reporter Queue", ["Dashboard", "Reporters", "Dispatch", "IR", "Ads"], [
                    {"type": "queue_item", "title": "Ravi K. · East Bangalore", "meta": "Kannada · ID uploaded", "buttons": [("Inc", SUCCESS), ("Dec", ACCENT)]},
                ], "Admin Inclines or Declines application"),
            ],
            [
                _phone(4, "Credentials", [
                    {"type": "card", "title": "Press ID Card", "lines": ["QR verified · Beat: East", "Valid 2026"], "badge": "Active"},
                    {"type": "card", "title": "Appointment Letter", "lines": ["Download PDF · Area assigned"]},
                ], "ID card & letter unlocked"),
                _phone(5, "Create", [
                    {"type": "field", "placeholder": "Headline & story body"},
                    {"type": "media", "icon": "IMG", "label": "Photo / Video / Audio"},
                    {"type": "actions", "buttons": [("Submit", PRIMARY), ("Draft", MUTED)]},
                ], "Create dispatch with attachments"),
                _admin(6, "Dispatch Review", ["Dashboard", "Reporters", "Dispatch", "IR", "Audit"], [
                    {"type": "queue_item", "title": "New dispatch · Pending", "meta": "Reporter · Bangalore · News", "buttons": [("Inc", SUCCESS), ("Dec", ACCENT)]},
                ], "Editorial Incline → live on feed"),
            ],
        ],
    },
    {
        "title": "Flow 3 — Premium User Posts News (Upload & Approval)",
        "subtitle": "Upload photo/video  ·  Admin checks  ·  Incline or Decline  ·  No auto-publish",
        "one_liner": (
            "A Premium member uploads photo or video news from their phone; "
            "admin must approve (Incline) before it appears in the feed for everyone."
        ),
        "rows": [
            [
                _phone(1, "Create", [
                    {"type": "status", "text": "Premium · Post enabled", "bg": "#faf5ff", "color": "#6b46c1"},
                    {"type": "media", "icon": "IMG", "label": "Upload images / video"},
                    {"type": "field", "placeholder": "Describe what you witnessed"},
                ], "User uploads news media"),
                _phone(2, "Submitted", [
                    {"type": "status", "text": "Pending Editorial Review", "bg": "#fefcbf", "color": "#975a16"},
                    {"type": "card", "title": "Your submission", "lines": ["Queued for true-news check", "Editorial review pending"]},
                ], "Enters shared review queue"),
                _admin(3, "Sub Admin Review", ["Dashboard", "Dispatch", "Reporters"], [
                    {"type": "queue_item", "title": "User tip · Traffic incident", "meta": "Video attached · Rajajinagar", "buttons": [("Inc", SUCCESS), ("Dec", ACCENT)]},
                ], "Sub Admin first-level check"),
            ],
            [
                _admin(4, "Admin Final", ["Dashboard", "Dispatch", "Audit"], [
                    {"type": "queue_item", "title": "Approved by Sub Admin", "meta": "Awaiting final Incline", "buttons": [("Inc", SUCCESS), ("Dec", ACCENT)]},
                ], "Admin final Incline or Decline"),
                _phone(5, "Published", [
                    {"type": "card", "title": "Your story is live", "lines": ["Attributed to you", "Visible in Bangalore feed"], "badge": "Verified"},
                    {"type": "actions", "buttons": [("View", PRIMARY), ("Share", MUTED)]},
                ], "Inclined → published with attribution"),
                _phone(6, "Declined", [
                    {"type": "status", "text": "Declined · See reason", "bg": "#fed7d7", "color": "#c53030"},
                    {"type": "card", "title": "Reason: Unverified", "lines": ["Add source & resubmit", "Editor note included"]},
                ], "Declined → feedback to user"),
            ],
        ],
    },
    {
        "title": "Flow 4 — Editorial Approval (True News Check)",
        "subtitle": "Review queue  ·  Preview story  ·  Incline or Decline  ·  Audit log",
        "one_liner": (
            "All news — from reporters or Premium users — waits in a queue until admin "
            "clicks Incline (publish) or Decline (reject); nothing goes live without this."
        ),
        "rows": [
            [
                _admin(1, "Review Queue", ["Dashboard", "Dispatch", "Audit"], [
                    {"type": "kpi", "items": [("12", "Pending"), ("48", "Today"), ("3", "Urgent")]},
                    {"type": "queue_item", "title": "Dispatch with video", "meta": "Source · City · Language", "buttons": [("Inc", SUCCESS), ("Dec", ACCENT)]},
                ], "All content lands in queue"),
                _admin(2, "Preview", ["Dispatch", "Media", "Meta"], [
                    {"type": "queue_item", "title": "Media preview pane", "meta": "Text · Photo · Video · Audio", "buttons": [("Inc", SUCCESS), ("Dec", ACCENT)]},
                ], "Reviewer inspects full dispatch"),
                _admin(3, "Decision", ["Dispatch", "Reasons"], [
                    {"type": "queue_item", "title": "Select reason if Decline", "meta": "Unverified · Off-topic · Duplicate", "buttons": [("Inc", SUCCESS), ("Dec", ACCENT)]},
                ], "Incline publish or Decline + note"),
            ],
            [
                _admin(4, "Audit Log", ["Audit", "Settings"], [
                    {"type": "timeline", "items": [{"text": "Inclined by Admin · 14:32", "done": True}, {"text": "Logged · immutable", "done": True}]},
                ], "Action recorded permanently"),
                _phone(5, "Feed", [
                    {"type": "card", "title": "Story now live", "lines": ["City + language filtered", "Endorse · Discuss"], "badge": "Verified"},
                ], "Published to correct feed"),
                _phone(6, "Notify", [
                    {"type": "card", "title": "Notification", "lines": ["Your dispatch was Inclined", "or Declined with reason"]},
                ], "Author notified instantly"),
            ],
        ],
    },
    {
        "title": "Flow 5 — Investigation Case (IR Tracking)",
        "subtitle": "Case number  ·  Assign teams  ·  Field reports  ·  Public status check",
        "one_liner": (
            "Admin opens an investigation with a unique case number; teams send reports; "
            "anyone can type that number in the app and see how the case is progressing."
        ),
        "rows": [
            [
                _admin(1, "Create IR", ["IR Center", "Teams"], [
                    {"type": "field", "placeholder": "IR-BLR-2026-00042 (auto)"},
                    {"type": "card", "title": "Case title", "lines": ["Assign IO · Select teams"]},
                ], "Auto-generated trackable IR#"),
                _admin(2, "Assign", ["IR Center", "Teams"], [
                    {"type": "queue_item", "title": "IO: Officer Sharma", "meta": "Team Alpha · Team Beta", "buttons": [("Save", PRIMARY), ("", MUTED)]},
                ], "Assign IO and field teams"),
                _admin(3, "Field Reports", ["IR Center", "Reports"], [
                    {"type": "timeline", "items": [{"text": "Team Alpha report in", "done": True}, {"text": "Team Beta pending", "done": False}]},
                ], "Teams submit field reports"),
            ],
            [
                _admin(4, "Consolidate", ["IR Center", "Reports"], [
                    {"type": "card", "title": "Master summary", "lines": ["IO merges all team findings"]},
                ], "IO consolidates into one report"),
                _phone(5, "Track IR", [
                    {"type": "field", "placeholder": "Enter IR number"},
                    {"type": "timeline", "items": [{"text": "Open", "done": True}, {"text": "In Progress", "done": True}, {"text": "Closed", "done": False}]},
                ], "Public tracker with timeline"),
                _admin(6, "Close IR", ["IR Center"], [
                    {"type": "status", "text": "Case Closed", "bg": "#c6f6d5", "color": "#276749"},
                ], "Admin closes investigation"),
            ],
        ],
    },
    {
        "title": "Flow 6 — Advertisements & Premium Membership",
        "subtitle": "Ads in feed  ·  Premium upgrade  ·  Earnings dashboard",
        "one_liner": (
            "Admin puts ads in the news feed; users can pay for Premium (extra benefits); "
            "reporters and creators can see how much they earned."
        ),
        "rows": [
            [
                _admin(1, "Ad Manager", ["Ads", "Analytics"], [
                    {"type": "queue_item", "title": "New campaign creative", "meta": "Feed Top · Bangalore", "buttons": [("Live", SUCCESS), ("Off", MUTED)]},
                ], "Admin creates & schedules ads"),
                _phone(2, "Feed + Ad", [
                    {"type": "card", "title": "Sponsored", "lines": ["Clearly labelled ad slot"]},
                    {"type": "card", "title": "News dispatch", "lines": ["Editorial content below"]},
                ], "Ads render in feed / Briefs"),
                _phone(3, "Go Premium", [
                    {"type": "status", "text": "★ Premium · Ad-free", "bg": "#faf5ff", "color": "#6b46c1"},
                    {"type": "actions", "buttons": [("Upgrade", ACCENT), ("Learn", MUTED)]},
                ], "User upgrades to Premium"),
            ],
            [
                _phone(4, "Profile", [
                    {"type": "stat_row", "items": [("2.4k", "Views"), ("186", "Endorse"), ("₹4.2k", "Earn")]},
                    {"type": "card", "title": "Earnings chart", "lines": ["Daily · Monthly breakdown"]},
                ], "Reporter / creator dashboard"),
                _admin(5, "Analytics", ["Analytics", "Payouts"], [
                    {"type": "kpi", "items": [("₹1.2L", "Revenue"), ("340", "Reporters"), ("89%", "Uptime")]},
                ], "Platform-wide analytics"),
            ],
        ],
    },
    {
        "title": "Flow 7 — Audio & Video Calls (Talk Inside App)",
        "subtitle": "Call button  ·  Ring  ·  Live talk  ·  Group calls  ·  Call history",
        "one_liner": (
            "Users, reporters, and editors can make audio or video calls inside the app "
            "to discuss news or work together — no need to switch to WhatsApp."
        ),
        "rows": [
            [
                _phone(1, "Profile", [
                    {"type": "card", "title": "Reporter · East BLR", "lines": ["Verified · Active beat"]},
                    {"type": "actions", "buttons": [("Audio", PRIMARY), ("Video", ACCENT)]},
                ], "Open contact → choose call type"),
                _phone(2, "Ringing", [
                    {"type": "status", "text": "Calling editor...", "bg": "#ebf8ff", "color": "#2b6cb0"},
                    {"type": "card", "title": "Incoming ring", "lines": ["SignalR push to recipient"]},
                ], "Recipient receives ring alert"),
                _phone(3, "Live Call", [
                    {"type": "media", "icon": "LIVE", "label": "Video / Audio stream"},
                    {"type": "actions", "buttons": [("Mute", MUTED), ("End", ACCENT)]},
                ], "WebRTC session — talk together"),
            ],
            [
                _phone(4, "Group Call", [
                    {"type": "card", "title": "IR Team Alpha", "lines": ["3 participants", "Investigation sync"]},
                    {"type": "actions", "buttons": [("Join", SUCCESS), ("Leave", ACCENT)]},
                ], "Team group audio/video call"),
                _phone(5, "History", [
                    {"type": "card", "title": "Recent calls", "lines": ["Editor · 12 min · Today", "Team IR · 8 min · Yesterday"]},
                ], "Call log in profile"),
            ],
        ],
    },
    {
        "title": "Flow 8 — AI News View (Original vs AI Tabs)",
        "subtitle": "Inside article page  ·  Two tabs  ·  Gemini or GPT  ·  Generated on publish",
        "one_liner": (
            "When reading a published story, the user switches between Original (reporter text) "
            "and AI View (simple summary / translation) using two tabs on the same article page."
        ),
        "rows": [
            [
                _phone(1, "Article", [
                    {"type": "tabs", "items": ["Original", "AI View"], "active": 0},
                    {"type": "card", "title": "Metro expansion approved", "lines": ["Full reporter dispatch text", "Source cited · Verified"], "badge": "Verified"},
                    {"type": "media", "icon": "▶", "label": "Field video"},
                ], "Default tab: Original published text"),
                _phone(2, "Article", [
                    {"type": "tabs", "items": ["Original", "AI View"], "active": 1},
                    {"type": "card", "title": "AI Summary", "lines": ["Plain-language recap", "Key points in bullets"]},
                    {"type": "status", "text": "AI-generated · Gemini/GPT", "bg": "#faf5ff", "color": "#6b46c1"},
                ], "Switch tab → AI simplified version"),
                _admin(3, "AI Settings", ["Settings", "AI", "Audit"], [
                    {"type": "field", "placeholder": "Provider: Gemini or OpenAI GPT"},
                    {"type": "field", "placeholder": "API key (server-side only)"},
                    {"type": "card", "title": "On publish", "lines": ["Auto-generate AI version", "Store with dispatch"]},
                ], "Admin configures AI provider & key"),
            ],
        ],
    },
]


def build_flow_sections(content_width):
    """Return list of FlowSection flowables."""
    return [
        FlowSection(
            flow["title"],
            flow["subtitle"],
            flow["one_liner"],
            flow["rows"],
            content_width,
        )
        for flow in FLOW_DEFINITIONS
    ]


def get_flow_summary_table():
    """Return rows for PDF 'Flows at a Glance' table: [Flow#, Title, One line]."""
    rows = [["Flow", "Name", "One-Line Explanation (Simple)"]]
    for flow in FLOW_DEFINITIONS:
        num = flow["title"].split("—")[0].strip().replace("Flow ", "")
        name = flow["title"].split("—", 1)[1].strip() if "—" in flow["title"] else flow["title"]
        rows.append([num, name, flow["one_liner"]])
    return rows


class SystemArchitectureDiagram(Flowable):
    """Visual system architecture for section 10."""

    def __init__(self, width):
        Flowable.__init__(self)
        self.width = width
        self.height = 9.5 * cm

    def _box(self, c, x, y, w, h, title, sub, fill, light_text=False):
        c.setFillColor(fill)
        c.setStrokeColor(CARD_BORDER)
        c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
        c.setFillColor(WHITE if light_text else PRIMARY)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + w / 2, y + h - 12, title)
        c.setFillColor(colors.HexColor("#e2e8f0") if light_text else MUTED)
        c.setFont("Helvetica", 6.5)
        for i, line in enumerate(sub[:2]):
            c.drawCentredString(x + w / 2, y + h - 22 - i * 9, line)

    def draw(self):
        c = self.canv
        w = self.width
        bw = (w - 1.2 * cm) / 3
        top_y = self.height - 1.6 * cm

        self._box(c, 0, top_y, bw, 1.4 * cm, "Consumer App", "Feed · Briefs · Profile", LIGHT_BG)
        self._box(c, bw + 0.6 * cm, top_y, bw, 1.4 * cm, "Reporter Portal", "Register · Dispatch · ID", LIGHT_BG)
        self._box(c, 2 * (bw + 0.6 * cm), top_y, bw, 1.4 * cm, "Admin Portal", "Incline · IR · Ads", LIGHT_BG)

        for i in range(3):
            cx = i * (bw + 0.6 * cm) + bw / 2
            c.setFillColor(ACCENT)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(cx, top_y - 0.35 * cm, "↓")

        api_y = top_y - 1.1 * cm
        self._box(c, w * 0.2, api_y, w * 0.6, 1.2 * cm, "API Layer (.NET GraphQL)", "Auth · Upload · Workflows", PRIMARY, light_text=True)

        c.setFillColor(ACCENT)
        c.drawCentredString(w / 2, api_y - 0.35 * cm, "↓")

        db_y = api_y - 1.1 * cm
        c.setFillColor(colors.HexColor("#2d3748"))
        c.roundRect(w * 0.25, db_y, w * 0.5, 1 * cm, 5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(w / 2, db_y + 0.38 * cm, "PostgreSQL Database")
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(w / 2, db_y + 0.15 * cm, "Users · Dispatches · IR · Audit")

        # Publish path
        path_y = 1.2 * cm
        c.setFillColor(LIGHT_BG)
        c.roundRect(0, path_y, w, 1.5 * cm, 5, fill=1, stroke=1)
        c.setStrokeColor(ACCENT)
        c.setFillColor(PRIMARY)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(8, path_y + 1.15 * cm, "Content Publish Path")
        steps = ["Submit", "Pending Review", "Incline", "Published Feed"]
        colors_path = [MUTED, WARNING, SUCCESS, PRIMARY]
        sx = 8
        for i, (step, col) in enumerate(zip(steps, colors_path)):
            c.setFillColor(col)
            c.roundRect(sx, path_y + 0.35 * cm, 2.8 * cm, 0.55 * cm, 3, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 6.5)
            c.drawCentredString(sx + 1.4 * cm, path_y + 0.5 * cm, step)
            sx += 3.1 * cm
            if i < 3:
                c.setFillColor(ACCENT)
                c.setFont("Helvetica-Bold", 9)
                c.drawCentredString(sx - 0.15 * cm, path_y + 0.5 * cm, "→")

        c.setFillColor(ACCENT)
        c.setFont("Helvetica", 6.5)
        c.drawString(8, path_y + 0.08 * cm, "Decline branch → author notified with reason code (parallel to Incline)")
