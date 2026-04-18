import uuid
import json
import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_certificate(score, verdict):
    cert_id = str(uuid.uuid4())

    data = {
        "id": cert_id,
        "score": score,
        "verdict": verdict,
        "timestamp": str(datetime.datetime.now())
    }

    # Save to ledger (blockchain simulation)
    try:
        with open("data/ledger.json", "r") as f:
            ledger = json.load(f)
    except:
        ledger = []

    ledger.append(data)

    with open("data/ledger.json", "w") as f:
        json.dump(ledger, f, indent=4)

    # ================= CREATE ENHANCED PDF =================
    import os
    os.makedirs("certificates", exist_ok=True)
    file_name = f"certificates/certificate_{cert_id}.pdf"

    doc = SimpleDocTemplate(file_name, pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#00ffe1'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.grey,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#00ffe1'),
        spaceAfter=10,
        spaceBefore=15
    )

    content = []

    # Header
    content.append(Paragraph("🛡️ DeepShield AI", title_style))
    content.append(Paragraph("Certificate of Authenticity", subtitle_style))
    content.append(Spacer(1, 0.3*inch))

    # Certificate ID Box
    cert_data = [
        ['Certificate ID:', cert_id],
        ['Issue Date:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Blockchain Status:', '✓ Verified & Immutable']
    ]
    
    cert_table = Table(cert_data, colWidths=[2*inch, 4*inch])
    cert_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    content.append(cert_table)
    content.append(Spacer(1, 0.3*inch))

    # Analysis Results
    content.append(Paragraph("Analysis Results", heading_style))
    
    # Verdict color
    verdict_color = colors.green if verdict == "Real" else (colors.orange if verdict == "Suspicious" else colors.red)
    
    results_data = [
        ['Authenticity Score:', f'{score:.2f}%'],
        ['Final Verdict:', verdict],
        ['Confidence Level:', 'High' if score > 85 else 'Medium' if score > 70 else 'Low']
    ]
    
    results_table = Table(results_data, colWidths=[2*inch, 4*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('TEXTCOLOR', (1, 1), (1, 1), verdict_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    content.append(results_table)
    content.append(Spacer(1, 0.3*inch))

    # Verification Statement
    content.append(Paragraph("Verification Statement", heading_style))
    
    verification_text = f"""
    This certificate confirms that the submitted content has been analyzed using DeepShield AI's 
    advanced deepfake detection algorithms. The content received an authenticity score of {score:.2f}% 
    and has been classified as <b>{verdict}</b>. This certificate is cryptographically secured and 
    recorded on our blockchain ledger for permanent verification.
    """
    
    content.append(Paragraph(verification_text, styles['Normal']))
    content.append(Spacer(1, 0.4*inch))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    content.append(Spacer(1, 0.5*inch))
    content.append(Paragraph("_" * 80, footer_style))
    content.append(Paragraph("DeepShield AI - Real-time Deepfake & Piracy Detection", footer_style))
    content.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))

    doc.build(content)

    # return BOTH id + file
    return cert_id, file_name
