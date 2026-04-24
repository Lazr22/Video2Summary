import os
import time
from database import get_record

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_to_txt(record_id: int) -> str | None:
    record = get_record(record_id)
    if not record:
        return None
    path = os.path.join(EXPORT_DIR, f"summary_{record_id}.txt")
    created = time.strftime("%Y-%m-%d %H:%M", time.localtime(record["created_at"]))
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"VIDEO2SUMMARY — Export\n{'='*50}\n\n")
        f.write(f"File: {record['filename']}\n")
        f.write(f"Date: {created}\n")
        f.write(f"Language: {record['language']}\n")
        f.write(f"Duration: {record['duration']}s\n")
        f.write(f"Word Count: {record['word_count']} words\n\n")
        f.write(f"SUMMARY\n{'-'*50}\n{record['summary']}\n\n")
        f.write(f"FULL TRANSCRIPT\n{'-'*50}\n{record['transcript']}\n")
    return path


def export_to_pdf(record_id: int) -> str | None:
    record = get_record(record_id)
    if not record:
        return None

    path = os.path.join(EXPORT_DIR, f"summary_{record_id}.pdf")
    created = time.strftime("%Y-%m-%d %H:%M", time.localtime(record["created_at"]))

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib.enums import TA_LEFT

        doc = SimpleDocTemplate(
            path, pagesize=A4,
            leftMargin=2*cm, rightMargin=2*cm,
            topMargin=2*cm, bottomMargin=2*cm
        )

        title_style = ParagraphStyle(
            "title", fontSize=20, fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1a1a2e"), spaceAfter=6
        )
        meta_style = ParagraphStyle(
            "meta", fontSize=10, fontName="Helvetica",
            textColor=colors.HexColor("#666666"), spaceAfter=4
        )
        heading_style = ParagraphStyle(
            "heading", fontSize=13, fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1a1a2e"), spaceBefore=14, spaceAfter=6
        )
        body_style = ParagraphStyle(
            "body", fontSize=11, fontName="Helvetica",
            leading=17, textColor=colors.HexColor("#333333"), spaceAfter=4
        )

        def safe(text):
            return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        story = [
            Paragraph("Video2Summary", title_style),
            Paragraph(f"<b>File:</b> {safe(record['filename'])}", meta_style),
            Paragraph(
                f"<b>Date:</b> {created} &nbsp;&nbsp;"
                f"<b>Language:</b> {safe(record['language'])} &nbsp;&nbsp;"
                f"<b>Duration:</b> {record['duration']}s &nbsp;&nbsp;"
                f"<b>Words:</b> {record['word_count']}",
                meta_style
            ),
            HRFlowable(width="100%", thickness=1,
                       color=colors.HexColor("#dddddd"), spaceAfter=12),
            Paragraph("Summary", heading_style),
            Paragraph(safe(record["summary"]), body_style),
            Spacer(1, 0.4*cm),
            HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd")),
            Paragraph("Full Transcript", heading_style),
            Paragraph(safe(record["transcript"]), body_style),
        ]

        doc.build(story)
        return path

    except ImportError:
        # ReportLab not installed — fall back to TXT
        return export_to_txt(record_id)

    except Exception as e:
        # Any other error — clean up broken file and raise
        if os.path.exists(path):
            os.remove(path)
        raise RuntimeError(f"PDF generation failed: {e}")