from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_report(
    output_path: str,
    filename: str,
    match_score: float,
    ats_score: float,
    missing_skills: list,
    llm_feedback: dict,
):
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    story = []

    story.append(Paragraph("Resume Analysis Report", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(f"<b>Resume:</b> {filename}", styles["Normal"])
    )

    story.append(
        Paragraph(
            f"<b>Match Score:</b> {match_score:.2f}%",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {ats_score:.2f}%",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Missing Skills", styles["Heading2"]))

    if missing_skills:
        for skill in missing_skills:
            story.append(
                Paragraph(f"• {skill}", styles["Normal"])
            )
    else:
        story.append(
            Paragraph(
                "No missing skills identified.",
                styles["Normal"],
            )
        )

    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("LLM Feedback", styles["Heading2"]))

    for section in [
        "strengths",
        "weaknesses",
        "missing_skills",
        "suggestions",
    ]:
        values = llm_feedback.get(section, [])

        story.append(
            Paragraph(
                section.replace("_", " ").title(),
                styles["Heading3"],
            )
        )

        for value in values:
            story.append(
                Paragraph(f"• {value}", styles["Normal"])
            )

    summary = llm_feedback.get("overall_summary")

    if summary:
        story.append(Spacer(1, 0.2 * inch))
        story.append(
            Paragraph("Overall Summary", styles["Heading2"])
        )
        story.append(
            Paragraph(summary, styles["Normal"])
        )

    doc.build(story)
