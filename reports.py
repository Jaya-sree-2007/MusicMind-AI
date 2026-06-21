from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from db import get_user_history

import os

# ==========================
# GENERATE PDF REPORT
# ==========================

def generate_pdf(username):

    filename = f"{username}_report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    # ----------------------
    # TITLE
    # ----------------------

    title = Paragraph(
        "MusicMind AI Personality Report",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    # ----------------------
    # USER NAME
    # ----------------------

    user_para = Paragraph(
        f"<b>Student:</b> {username}",
        styles["Normal"]
    )

    elements.append(user_para)
    elements.append(Spacer(1, 15))

    # ----------------------
    # FETCH HISTORY
    # ----------------------

    history = get_user_history(username)

    if len(history) == 0:

        elements.append(
            Paragraph(
                "No Analysis Records Found",
                styles["Normal"]
            )
        )

    else:

        for row in history:

            elements.append(
                Paragraph(
                    f"<b>Personality:</b> {row['personality']}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Genre:</b> {row['genre']}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Score:</b> {row['score']}%",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Date:</b> {row['created_at']}",
                    styles["Normal"]
                )
            )

            elements.append(
                Spacer(1, 10)
            )

    # ----------------------
    # BUILD PDF
    # ----------------------

    doc.build(elements)

    return filename