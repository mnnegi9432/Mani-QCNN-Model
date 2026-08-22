from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.graphics.shapes import Drawing, Rect, String

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

from datetime import datetime

import os


# ==========================================================
# HYBRID QCNN PDF REPORT
# ==========================================================

def create_report(
    prediction,
    confidence,
    filename,
    image_path=None,
    features=None,
    symptoms=None,
    recommendation=""
):

    # -----------------------------------------
    # Create Report Folder
    # -----------------------------------------

    report_folder = "static/reports"

    os.makedirs(report_folder, exist_ok=True)

    pdf_path = os.path.join(
        report_folder,
        "Brain_Tumor_Report.pdf"
    )

    # -----------------------------------------
    # PDF
    # -----------------------------------------

    doc = SimpleDocTemplate(

        pdf_path,

        pagesize=(8.27 * inch, 11.69 * inch),

        leftMargin=25,
        rightMargin=25,
        topMargin=25,
        bottomMargin=25

    )

    styles = getSampleStyleSheet()

    story = []

    # -----------------------------------------
    # Styles
    # -----------------------------------------

    title = styles["Title"]

    title.alignment = TA_CENTER

    title.fontSize = 22

    title.textColor = HexColor("#0B5394")


    heading = styles["Heading2"]

    heading.textColor = HexColor("#0B5394")

    heading.fontSize = 15


    normal = styles["BodyText"]

    normal.fontSize = 11

    normal.leading = 18

    # -----------------------------------------
    # Header
    # -----------------------------------------

    story.append(

        Paragraph(

            "<b>Hybrid Quantum Brain Tumor Detection System</b>",

            title

        )

    )

    story.append(

        Paragraph(

            "<b>Hybrid QCNN Diagnostic Report</b>",

            heading

        )

    )

    story.append(

        Paragraph(

            "Artificial Intelligence Assisted Brain Tumor Classification",

            normal

        )

    )

    story.append(Spacer(1,15))
        # ==========================================================
    # MRI IMAGE
    # ==========================================================

    if image_path and os.path.exists(image_path):

        img = Image(image_path)

        img.drawWidth = 2.8 * inch

        img.drawHeight = 2.8 * inch

    else:

        img = Paragraph(

            "<b>No MRI Image Available</b>",

            normal

        )


    # ==========================================================
    # DATE & TIME
    # ==========================================================

    current_date = datetime.now().strftime("%d-%B-%Y")

    current_time = datetime.now().strftime("%I:%M %p")


    # ==========================================================
    # PREDICTION SUMMARY TABLE
    # ==========================================================

    summary = [

        ["Prediction", prediction],

        ["Confidence", f"{float(confidence):.2f}%"],

        ["Date", current_date],

        ["Time", current_time],

        ["Model", "Hybrid QCNN"],

        ["Feature Extractor", "EfficientNet-B0"],

        ["Normalization", "StandardScaler"],

        ["Feature Reduction", "PCA (1280 → 16)"]

    ]

    summary_table = Table(

        summary,

        colWidths=[2.2 * inch, 3.2 * inch]

    )

    summary_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.8,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),HexColor("#EAF2FF")),

            ("TEXTCOLOR",(0,0),(0,-1),HexColor("#0B5394")),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

            ("FONTSIZE",(0,0),(-1,-1),10),

            ("BOTTOMPADDING",(0,0),(-1,-1),7),

            ("TOPPADDING",(0,0),(-1,-1),7)

        ])

    )


    # ==========================================================
    # IMAGE + SUMMARY
    # ==========================================================

    story.append(

        Paragraph(

            "<b>Prediction Summary</b>",

            heading

        )

    )

    story.append(Spacer(1,8))

    prediction_table = Table(

        [[img, summary_table]],

        colWidths=[3.0*inch,3.8*inch]

    )

    prediction_table.setStyle(

        TableStyle([

            ("VALIGN",(0,0),(-1,-1),"TOP"),

            ("BOTTOMPADDING",(0,0),(-1,-1),10)

        ])

    )

    story.append(prediction_table)

    story.append(Spacer(1,18))


    # ==========================================================
    # CONFIDENCE BAR
    # ==========================================================

    story.append(

        Paragraph(

            "<b>Prediction Confidence</b>",

            heading

        )

    )

    story.append(Spacer(1,6))

    confidence = float(confidence)

    if confidence < 0:
        confidence = 0

    if confidence > 100:
        confidence = 100

    bar = Drawing(430,30)

    bar.add(

        Rect(

            0,

            8,

            320,

            12,

            strokeColor=colors.grey,

            fillColor=colors.white

        )

    )

    bar.add(

        Rect(

            0,

            8,

            320 * (confidence / 100),

            12,

            strokeColor=HexColor("#28A745"),

            fillColor=HexColor("#28A745")

        )

    )

    bar.add(

        String(

            335,

            8,

            f"{confidence:.2f}%",

            fontSize=11,

            fillColor=HexColor("#0B5394")

        )

    )

    story.append(bar)

    story.append(Spacer(1,20))
        # ==========================================================
    # MRI CHARACTERISTICS
    # ==========================================================

    story.append(
        Paragraph(
            "<b>MRI Characteristics</b>",
            heading
        )
    )

    story.append(Spacer(1,6))

    if not features:
        features = ["No characteristics available."]

    feature_rows = []

    for item in features:
        feature_rows.append([f"• {item}"])

    feature_table = Table(
        feature_rows,
        colWidths=[6.8*inch]
    )

    feature_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.4,colors.lightgrey),

            ("BACKGROUND",(0,0),(-1,-1),HexColor("#F4FAFF")),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("FONTSIZE",(0,0),(-1,-1),10),

            ("BOTTOMPADDING",(0,0),(-1,-1),6),

            ("TOPPADDING",(0,0),(-1,-1),6)

        ])

    )

    story.append(feature_table)

    story.append(Spacer(1,15))


    # ==========================================================
    # CLINICAL SYMPTOMS
    # ==========================================================

    story.append(

        Paragraph(

            "<b>Clinical Symptoms</b>",

            heading

        )

    )

    story.append(Spacer(1,6))

    if not symptoms:
        symptoms = ["No symptoms available."]

    symptom_rows = []

    for item in symptoms:
        symptom_rows.append([f"• {item}"])

    symptom_table = Table(

        symptom_rows,

        colWidths=[6.8*inch]

    )

    symptom_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.4,colors.lightgrey),

            ("BACKGROUND",(0,0),(-1,-1),HexColor("#FFF8F2")),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("FONTSIZE",(0,0),(-1,-1),10),

            ("BOTTOMPADDING",(0,0),(-1,-1),6),

            ("TOPPADDING",(0,0),(-1,-1),6)

        ])

    )

    story.append(symptom_table)

    story.append(Spacer(1,15))


    # ==========================================================
    # RECOMMENDATION
    # ==========================================================

    story.append(

        Paragraph(

            "<b>Recommendation</b>",

            heading

        )

    )

    story.append(Spacer(1,6))

    recommendation_table = Table(

        [[recommendation]],

        colWidths=[6.8*inch]

    )

    recommendation_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.8,colors.orange),

            ("BACKGROUND",(0,0),(-1,-1),HexColor("#FFF8DD")),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("FONTSIZE",(0,0),(-1,-1),10),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(recommendation_table)

    story.append(Spacer(1,18))


    # ==========================================================
    # MODEL PIPELINE
    # ==========================================================

    story.append(

        Paragraph(

            "<b>Hybrid QCNN Model Pipeline</b>",

            heading

        )

    )

    story.append(Spacer(1,8))

    pipeline = [

        ["MRI Image"],

        ["↓"],

        ["EfficientNet-B0"],

        ["↓"],

        ["StandardScaler"],

        ["↓"],

        ["PCA (1280 → 16)"],

        ["↓"],

        ["Angle Encoding"],

        ["↓"],

        ["Hybrid QCNN"],

        ["↓"],

        ["Softmax Classifier"],

        ["↓"],

        ["Brain Tumor Prediction"]

    ]

    pipeline_table = Table(

        pipeline,

        colWidths=[6.8*inch]

    )

    pipeline_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(-1,-1),HexColor("#EEF7FF")),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

            ("FONTSIZE",(0,0),(-1,-1),10),

            ("BOTTOMPADDING",(0,0),(-1,-1),6),

            ("TOPPADDING",(0,0),(-1,-1),6)

        ])

    )

    story.append(pipeline_table)

    story.append(Spacer(1,20))
        # ==========================================================
    # MODEL PERFORMANCE
    # ==========================================================

    story.append(
        Paragraph(
            "<b>Model Performance</b>",
            heading
        )
    )

    story.append(Spacer(1,8))

    performance = [

        ["Metric","Value"],

        ["Accuracy","94.31 %"],

        ["Precision","94.12 %"],

        ["Recall","94.08 %"],

        ["F1-Score","94.10 %"]

    ]

    performance_table = Table(

        performance,

        colWidths=[3.2*inch,3.2*inch]

    )

    performance_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.6,colors.grey),

            ("BACKGROUND",(0,0),(-1,0),HexColor("#0B5394")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(-1,-1),HexColor("#F8FBFF")),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

            ("FONTSIZE",(0,0),(-1,-1),10),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(performance_table)

    story.append(Spacer(1,18))


    # ==========================================================
    # REPORT INFORMATION
    # ==========================================================

    story.append(
        Paragraph(
            "<b>Report Information</b>",
            heading
        )
    )

    story.append(Spacer(1,8))

    generated = datetime.now().strftime("%d %B %Y  %I:%M %p")

    info = [

        ["Generated On", generated],

        ["Framework", "Hybrid QCNN"],

        ["Application", "Brain Tumor Detection using MRI"],

        ["Developer", "Manish Negi"],

        ["Organization", "Uttaranchal University"]

    ]

    info_table = Table(

        info,

        colWidths=[2.5*inch,4.1*inch]

    )

    info_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),HexColor("#EAF2FF")),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("FONTSIZE",(0,0),(-1,-1),10),

            ("BOTTOMPADDING",(0,0),(-1,-1),7),

            ("TOPPADDING",(0,0),(-1,-1),7)

        ])

    )

    story.append(info_table)

    story.append(Spacer(1,20))


    # ==========================================================
    # DISCLAIMER
    # ==========================================================

    story.append(
        Paragraph(
            "<b>Disclaimer</b>",
            heading
        )
    )

    story.append(Spacer(1,6))

    story.append(

        Paragraph(

            "This report has been automatically generated using the "
            "Hybrid Quantum Brain Tumor Detection System. The prediction "
            "is intended for research and educational purposes only and "
            "must not be considered a substitute for professional medical "
            "diagnosis. Clinical decisions should always be confirmed by "
            "a qualified radiologist or neurologist.",

            normal

        )

    )

    story.append(Spacer(1,20))


    # ==========================================================
    # FOOTER
    # ==========================================================

    story.append(

        Paragraph(

            "<para align='center'><font color='#0B5394'><b>Hybrid Quantum Brain Tumor Detection System</b></font></para>",

            normal

        )

    )

    story.append(

        Paragraph(

            "<para align='center'>© 2026 All Rights Reserved | Developed by <b>Manish Negi</b></para>",

            normal

        )

    )


    # ==========================================================
    # BUILD PDF
    # ==========================================================

    doc.build(story)

    return pdf_path