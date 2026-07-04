from io import BytesIO
from html import escape
from urllib.parse import urlparse, urlunparse

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def safe_text(value, default="Not available"):
    """
    Convert values to safe text for ReportLab Paragraphs.
    """

    if value is None:
        return escape(default)

    value = str(value).strip()

    if not value:
        return escape(default)

    return escape(value)


def clean_url(url):
    """
    Strip tracking query parameters and fragments from a URL
    for cleaner display in the report.
    """

    if not url:
        return ""

    try:
        parsed = urlparse(str(url).strip())
        return urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path, "", "", "")
        )
    except Exception:
        return str(url).strip()


def add_page_number(canvas, document):
    """
    Add footer and page number to every PDF page.
    """

    canvas.saveState()

    page_number = canvas.getPageNumber()

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)

    canvas.drawString(
        45,
        25,
        "AI Company Research Assistant",
    )

    canvas.drawRightString(
        A4[0] - 45,
        25,
        f"Page {page_number}",
    )

    canvas.restoreState()


def generate_company_report(
    analysis,
    competitors,
    search_results=None,
    crawled_pages=None,
):
    """
    Generate a professional PDF company research report
    and return the PDF as bytes.
    """

    search_results = search_results or []
    crawled_pages = crawled_pages or []

    buffer = BytesIO()

    company_name = analysis.get(
        "company_name",
        "Company",
    )

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
        title=f"{company_name} Research Report",
        author="AI Company Research Assistant",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=10,
        textColor=colors.HexColor("#1F4E79"),
    )

    company_title_style = ParagraphStyle(
        "CompanyTitle",
        parent=styles["Heading1"],
        fontSize=19,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        spaceBefore=12,
        spaceAfter=10,
        textColor=colors.HexColor("#1F4E79"),
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=8,
        textColor=colors.HexColor("#34495E"),
    )

    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["BodyText"],
        fontSize=10,
        leading=16,
        spaceAfter=8,
    )

    bullet_style = ParagraphStyle(
        "BulletCustom",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-8,
        spaceAfter=6,
    )

    source_style = ParagraphStyle(
        "SourceStyle",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=13,
        leftIndent=10,
        spaceAfter=7,
        textColor=colors.HexColor("#333333"),
    )

    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["BodyText"],
        fontSize=8,
        leading=12,
        textColor=colors.grey,
        spaceBefore=10,
    )

    story = []

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    story.append(
        Paragraph(
            "AI Company Research Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            safe_text(company_name),
            company_title_style,
        )
    )

    story.append(
        Paragraph(
            "Generated using AI-powered web research, "
            "website crawling, public information analysis, "
            "and competitor research.",
            subtitle_style,
        )
    )

    story.append(Spacer(1, 10))


    # --------------------------------------------------
    # COMPANY INFORMATION
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Company Information",
            heading_style,
        )
    )

    company_data = [
        [
            Paragraph("<b>Company Name</b>", body_style),
            Paragraph(
                safe_text(
                    analysis.get("company_name")
                ),
                body_style,
            ),
        ],
        [
            Paragraph("<b>Website</b>", body_style),
            Paragraph(
                safe_text(
                    analysis.get("website")
                ),
                body_style,
            ),
        ],
        [
            Paragraph("<b>Phone Number</b>", body_style),
            Paragraph(
                safe_text(
                    analysis.get("phone_number")
                ),
                body_style,
            ),
        ],
        [
            Paragraph("<b>Address</b>", body_style),
            Paragraph(
                safe_text(
                    analysis.get("address")
                ),
                body_style,
            ),
        ],
        [
            Paragraph("<b>Industry</b>", body_style),
            Paragraph(
                safe_text(
                    analysis.get("industry")
                ),
                body_style,
            ),
        ],
        [
            Paragraph("<b>Country</b>", body_style),
            Paragraph(
                safe_text(
                    analysis.get("country")
                ),
                body_style,
            ),
        ],
    ]

    company_table = Table(
        company_data,
        colWidths=[
            1.7 * inch,
            4.7 * inch,
        ],
    )

    company_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#EAF2F8"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.lightgrey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(company_table)

    story.append(Spacer(1, 18))


    # --------------------------------------------------
    # COMPANY SUMMARY
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Company Summary",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            safe_text(
                analysis.get(
                    "company_summary"
                )
            ),
            body_style,
        )
    )


    # --------------------------------------------------
    # PRODUCTS AND SERVICES
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Products & Services",
            heading_style,
        )
    )

    products = analysis.get(
        "products_services",
        [],
    )

    if products:

        for product in products:

            story.append(
                Paragraph(
                    f"• {safe_text(product)}",
                    bullet_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "No products or services available.",
                body_style,
            )
        )


    # --------------------------------------------------
    # PAIN POINTS
    # --------------------------------------------------

    story.append(
        Paragraph(
            "AI-Generated Pain Points",
            heading_style,
        )
    )

    pain_points = analysis.get(
        "pain_points",
        [],
    )

    if pain_points:

        for pain_point in pain_points:

            story.append(
                Paragraph(
                    f"• {safe_text(pain_point)}",
                    bullet_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "No pain points available.",
                body_style,
            )
        )

    story.append(
        Paragraph(
            "Note: Pain points are AI-generated inferences "
            "based on collected company and industry information "
            "and should not be interpreted as verified company statements.",
            disclaimer_style,
        )
    )


    # --------------------------------------------------
    # COMPETITOR ANALYSIS
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Competitor Analysis",
            heading_style,
        )
    )

    if competitors:

        competitor_data = [
            [
                Paragraph(
                    "<b><font color='white'>Company Name</font></b>",
                    body_style,
                ),
                Paragraph(
                    "<b><font color='white'>Website</font></b>",
                    body_style,
                ),
            ]
        ]

        for competitor in competitors:

            competitor_name = safe_text(
                competitor.get(
                    "company_name"
                )
            )

            competitor_url = clean_url(
                competitor.get(
                    "website",
                    "",
                )
            )

            if competitor_url:

                escaped_url = escape(
                    competitor_url,
                    quote=True,
                )

                website_paragraph = Paragraph(
                    f'<link href="{escaped_url}" '
                    f'color="#1F4E79">'
                    f'{escape(competitor_url)}</link>',
                    body_style,
                )

            else:

                website_paragraph = Paragraph(
                    "Not available",
                    body_style,
                )

            competitor_data.append(
                [
                    Paragraph(
                        competitor_name,
                        body_style,
                    ),
                    website_paragraph,
                ]
            )

        competitor_table = Table(
            competitor_data,
            colWidths=[
                2.2 * inch,
                4.2 * inch,
            ],
            repeatRows=1,
        )

        competitor_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1F4E79"),
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.lightgrey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        story.append(competitor_table)

    else:

        story.append(
            Paragraph(
                "No validated competitors were found.",
                body_style,
            )
        )


    # --------------------------------------------------
    # SOURCES AND REFERENCES
    # --------------------------------------------------

    story.append(PageBreak())

    story.append(
        Paragraph(
            "Sources & References",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The following publicly available sources were "
            "collected during the company research process.",
            body_style,
        )
    )

    source_urls = set()

    # --------------------------------------------------
    # CRAWLED WEBSITE PAGES
    # --------------------------------------------------

    if crawled_pages:

        story.append(
            Paragraph(
                "Company Website Pages",
                subheading_style,
            )
        )

        for page in crawled_pages:

            page_url = clean_url(
                page.get(
                    "url",
                    "",
                )
            )

            if (
                page_url
                and page_url not in source_urls
            ):

                source_urls.add(page_url)

                escaped_url = escape(
                    page_url,
                    quote=True,
                )

                story.append(
                    Paragraph(
                        f'• <link href="{escaped_url}" '
                        f'color="#1F4E79">'
                        f'{escape(page_url)}</link>',
                        source_style,
                    )
                )


    # --------------------------------------------------
    # PUBLIC WEB SOURCES
    # --------------------------------------------------

    if search_results:

        story.append(
            Paragraph(
                "Public Web Sources",
                subheading_style,
            )
        )

        displayed_sources = 0

        for result in search_results:

            title = str(
                result.get(
                    "title",
                    "Research Source",
                )
            ).strip()

            link = clean_url(
                result.get(
                    "link",
                    "",
                )
            )

            if (
                link
                and link not in source_urls
            ):

                source_urls.add(link)

                escaped_link = escape(
                    link,
                    quote=True,
                )

                story.append(
                    Paragraph(
                        f'• <b>{escape(title)}</b><br/>'
                        f'<link href="{escaped_link}" '
                        f'color="#1F4E79">'
                        f'{escape(link)}</link>',
                        source_style,
                    )
                )

                displayed_sources += 1

            if displayed_sources >= 10:
                break


    if not source_urls:

        story.append(
            Paragraph(
                "No research sources were available.",
                body_style,
            )
        )


    # --------------------------------------------------
    # METHODOLOGY NOTE
    # --------------------------------------------------

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Research Methodology",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "This report combines automated web search, "
            "official website crawling, public information "
            "collection, AI-assisted structured analysis, "
            "and competitor research. AI-generated insights "
            "may contain inaccuracies and should be independently "
            "verified before use in business-critical decisions.",
            body_style,
        )
    )


    # --------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes