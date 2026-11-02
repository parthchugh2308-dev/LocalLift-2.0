import os, sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "LocalLift 2.0 — Complete Platform Architecture & Layman Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 34, "LocalLift 2.0 • Pan-India Hyperlocal Neighborhood Marketplace")
        page_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 34, page_text)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#E11D48")
    dark_slate = colors.HexColor("#0F172A")
    body_color = colors.HexColor("#334155")
    bg_tint = colors.HexColor("#FFF1F3")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=dark_slate,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=body_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=body_color,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TH',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TC',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=dark_slate
    )

    table_cell_bold = ParagraphStyle(
        'TCB',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=dark_slate
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#9F1239")
    )

    story = []

    # ── HEADER TITLE BLOCK ─────────────────────────────────────────────
    story.append(Paragraph("LocalLift 2.0 — Complete Project Guide", title_style))
    story.append(Paragraph("A Plain-English Deep Dive: What We Built, Differentiators, Layman Tech Stack, and End-to-End Workflow", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=12))

    # ── EXECUTIVE SUMMARY / WHAT WE HAVE MADE ──────────────────────────
    story.append(Paragraph("1. What Have We Made? (In 60 Seconds)", h1_style))
    story.append(Paragraph(
        "<b>LocalLift 2.0</b> is a modern, GPS-driven neighborhood marketplace platform built to connect real local "
        "merchants (corner kiranas, authentic bakeries, pharmacies, sweet shops, boutique clothiers) directly with nearby customers. "
        "Unlike quick-commerce delivery apps that push corporate dark warehouses, LocalLift digitizes and empowers existing "
        "Indian small-business shopkeepers.",
        body_style
    ))
    story.append(Paragraph(
        "The system operates across <b>4 fully synchronized portals</b>:",
        body_style
    ))
    story.append(Paragraph("• <b>Customer PWA (/)</b>: Street-level GPS discovery across 16 categories, multi-vendor cart, COD & Razorpay, live rider tracking, and an AI shopping assistant.", bullet_style))
    story.append(Paragraph("• <b>Vendor Partner Portal (/vendor)</b>: Zero-commission storefront control, real-time stock toggles, Gemini AI catalog generator, and orders pipeline.", bullet_style))
    story.append(Paragraph("• <b>Delivery Fleet Cockpit (/delivery)</b>: Live GPS rider telemetry, trip management, double cryptographic OTP handshake (Pickup + Delivery), and auditable payouts.", bullet_style))
    story.append(Paragraph("• <b>Admin Control Center (/admin)</b>: Merchant approval governance, multi-city GMV analytics, commission tracking, refunds, and Executive Intelligence AI.", bullet_style))

    story.append(Spacer(1, 8))

    # ── WHAT IS NEW & DIFFERENT FROM OTHERS ────────────────────────────
    story.append(Paragraph("2. What Is New in Our Project Rather Than Others?", h1_style))
    story.append(Paragraph(
        "Here is how LocalLift stands apart from existing market giants like Blinkit, Zepto, Swiggy Instamart, and Amazon:",
        body_style
    ))

    diff_data = [
        [
            Paragraph("Capability", table_header),
            Paragraph("Quick-Commerce (Blinkit / Zepto)", table_header),
            Paragraph("Food Aggregators (Swiggy / Zomato)", table_header),
            Paragraph("LocalLift 2.0 (Our Platform)", table_header)
        ],
        [
            Paragraph("Who Sells the Goods?", table_cell_bold),
            Paragraph("Corporate Dark Warehouses", table_cell),
            Paragraph("Registered Restaurants", table_cell),
            Paragraph("Real Local Neighborhood Kiranas & Mom-and-Pop Shops", table_cell_bold)
        ],
        [
            Paragraph("Merchant Commission", table_cell_bold),
            Paragraph("N/A (They own the goods)", table_cell),
            Paragraph("Extremely High (25% to 35%)", table_cell),
            Paragraph("0% Zero Predatory Commission (Merchants keep 100%)", table_cell_bold)
        ],
        [
            Paragraph("Multi-Store Cart", table_cell_bold),
            Paragraph("Single warehouse only", table_cell),
            Paragraph("Order from 1 store at a time", table_cell),
            Paragraph("Multi-Vendor Checkout: Order bread, milk & medicine in 1 cart!", table_cell_bold)
        ],
        [
            Paragraph("Handoff Security", table_cell_bold),
            Paragraph("Unverified doorstep dropoffs", table_cell),
            Paragraph("Simple single delivery OTP", table_cell),
            Paragraph("Double OTP Handshake: Pickup OTP at store + Delivery OTP at home", table_cell_bold)
        ],
        [
            Paragraph("Built-in AI Ecosystem", table_cell_bold),
            Paragraph("Generic customer support bot", table_cell),
            Paragraph("Search autocomplete only", table_cell),
            Paragraph("Google Gemini 3.5 Flash: 17 role-scoped tools across all 4 portals", table_cell_bold)
        ],
        [
            Paragraph("Offline & Cloud Safety", table_cell_bold),
            Paragraph("App crashes without cloud", table_cell),
            Paragraph("App crashes without cloud", table_cell),
            Paragraph("Zero-downtime deterministic local rule fallback engine", table_cell_bold)
        ]
    ]

    diff_table = Table(diff_data, colWidths=[90, 130, 130, 154])
    diff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(diff_table)

    story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── TECH STACK IN LAYMAN'S LANGUAGE ────────────────────────────────
    story.append(Paragraph("3. Our Tech Stack — Explained in Plain English", h1_style))
    story.append(Paragraph(
        "Think of our technology stack like running a Michelin-star modern restaurant:",
        body_style
    ))

    tech_data = [
        [
            Paragraph("Technology", table_header),
            Paragraph("Restaurant Analogy", table_header),
            Paragraph("What It Actually Does in LocalLift 2.0", table_header)
        ],
        [
            Paragraph("Python & Flask 3.1", table_cell_bold),
            Paragraph("The Master Chef & Kitchen", table_cell),
            Paragraph("The core backend brain. Handles all HTTP requests, validates order prices, routes payments, enforces security rules, and calculates distance.", table_cell)
        ],
        [
            Paragraph("SQLite 3 Database", table_cell_bold),
            Paragraph("The Head Ledger & Safe", table_cell),
            Paragraph("The relational database. Holds all shops, products, order items, customer records, delivery telemetry, and financial audit logs with foreign-key guarantees.", table_cell)
        ],
        [
            Paragraph("Alpine.js & HTML5", table_cell_bold),
            Paragraph("The Fast Waiter", table_cell),
            Paragraph("The client-side interface. Keeps the app lightweight and lightning-fast. Updates cart counts, tabs, and modals instantly without reloading the page.", table_cell)
        ],
        [
            Paragraph("Tailwind CSS", table_cell_bold),
            Paragraph("The Interior Designer", table_cell),
            Paragraph("Our custom romantic, high-contrast theme (#E11D48 rose, tinted surface cards, modern typography). Makes the app look stunning on both mobile phones and desktops.", table_cell)
        ],
        [
            Paragraph("Leaflet.js & OpenStreetMap", table_cell_bold),
            Paragraph("The GPS Radar & Map", table_cell),
            Paragraph("Interactive street maps. Shows the customer's pulsing GPS marker, color-coded shop pins, and provides real-time live rider tracking.", table_cell)
        ],
        [
            Paragraph("Google Gemini 3.5 Flash", table_cell_bold),
            Paragraph("The Smart Executive Advisor", table_cell),
            Paragraph("Official Google Generative AI API. Powers natural language queries, generates authentic product catalogs, and provides business insights via 17 function tools.", table_cell)
        ],
        [
            Paragraph("Razorpay API", table_cell_bold),
            Paragraph("The Cashier / Digital Vault", table_cell),
            Paragraph("Processes UPI, debit/credit cards, and net banking with cryptographic HMAC-SHA256 signature verification and auditable refund handling.", table_cell)
        ],
        [
            Paragraph("Gunicorn WSGI", table_cell_bold),
            Paragraph("The Industrial Power Generator", table_cell),
            Paragraph("Production web server running on Render that serves concurrent requests securely without dropping connections.", table_cell)
        ]
    ]

    tech_table = Table(tech_data, colWidths=[100, 120, 284])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(tech_table)

    story.append(Spacer(1, 10))

    # ── FULL END-TO-END PROJECT WORKFLOW ───────────────────────────────
    story.append(Paragraph("4. Full End-to-End Project Workflow", h1_style))
    story.append(Paragraph(
        "Here is the exact journey of an order from customer click to doorstep completion:",
        body_style
    ))

    steps = [
        ("Step 1: Hyperlocal Discovery", "The customer opens LocalLift. The browser's Geolocation API detects their coordinates. The map centers on their street and reveals all verified local stores within their chosen radius (500m to 10km)."),
        ("Step 2: Multi-Store Basket Building", "The customer browses different shops. They can add Fresh Bread from Sharma Bakery and Whole Milk from Gupta Dairy into one basket. The client saves this basket into localStorage so it never disappears on page refresh."),
        ("Step 3: Server-Side Price & Stock Verification", "When the customer clicks 'Proceed to Pay', the server inspects every line item against database catalog prices to prevent client-side tampering, verifies merchant active status, and confirms both shops are within the serviceable city."),
        ("Step 4: Atomic Multi-Vendor Checkout", "The database creates 1 parent record in Order_Groups and 2 distinct child orders in Orders. If payment is COD, child orders are immediately set to 'pending' for dispatch. If Razorpay is chosen, a secure payment order is generated."),
        ("Step 5: Merchant Fulfillment", "Each merchant sees their specific order appear in their Vendor Dashboard (/vendor). The merchant begins preparing the parcel and clicks 'Ready for Pickup'."),
        ("Step 6: Delivery Partner Assignment & Pickup OTP", "An approved delivery rider logs into the Delivery Fleet Cockpit (/delivery). They view available unassigned orders and tap 'Accept Delivery'. When the rider arrives at the shop, they provide the Pickup OTP. The merchant enters the OTP into their dashboard to confirm the correct rider is picking up the parcel."),
        ("Step 7: Real-Time Live GPS Telemetry", "Once picked up, the rider's phone starts transmitting high-precision GPS coordinates over HTTPS to /api/delivery/location every few seconds. The customer opens their order tracking modal and watches the rider moving live toward their home on Leaflet."),
        ("Step 8: Doorstep Delivery OTP Verification", "The rider arrives at the customer's gate. The customer reads out their private 6-digit Delivery OTP (visible only on their phone). The rider submits the OTP, the server verifies the cryptographic HMAC-SHA256 hash, and the order is marked 'Delivered'."),
        ("Step 9: Financial Settlement & AI Auditing", "The rider's delivery compensation is credited to their Delivery_Earnings_Ledger. The platform commission and merchant net earnings are calculated. The Central Administrator can ask the Admin Intelligence AI: 'Show today's GMV and completed trips' to receive real-time metrics.")
    ]

    for title, desc in steps:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(Spacer(1, 10))

    # ── SECURITY & RESILIENCE ARCHITECTURE ─────────────────────────────
    story.append(Paragraph("5. Built-in Security & Resilience Safeguards", h1_style))
    story.append(Paragraph("• <b>Zero-Exposure Cryptographic OTPs</b>: Plaintext delivery OTPs are never stored in the database or exposed over public tracking APIs; only secure HMAC-SHA256 hashes are used.", bullet_style))
    story.append(Paragraph("• <b>Anti-Tampering Price Validation</b>: Every checkout re-verifies prices strictly on the server against the catalog; client-side price hacks are instantly rejected.", bullet_style))
    story.append(Paragraph("• <b>Auto-Derived Production Secret Key</b>: Cloud deployments on Render automatically derive persistent 256-bit cryptographic keys from service metadata, preventing startup crashes.", bullet_style))
    story.append(Paragraph("• <b>Dual-Engine AI Reliability</b>: If the Gemini API key is missing or internet is down, the platform falls back to a deterministic local rule engine—zero 500 errors, zero downtime.", bullet_style))
    story.append(Paragraph("• <b>10 Comprehensive Test Suites</b>: 91+ automated unit and integration tests verify every stage from database schema to multi-vendor checkout and financial ledgers.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")

if __name__ == '__main__':
    output_pdf = sys.argv[1] if len(sys.argv) > 1 else "LocalLift_Project_Guide.pdf"
    build_pdf(output_pdf)
