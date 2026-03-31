from fpdf import FPDF
import re

def clean_text(text: str) -> str:
    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
        "•": "-",
        "…": "...",
        "\u00A0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove unsupported unicode characters like emoji / Hindi / special symbols
    text = re.sub(r"[^\x00-\xff]", "", text)

    return text


def save_to_pdf(text: str, filename: str = "output/summary.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    safe_text = clean_text(text)

    for line in safe_text.split("\n"):
        line = line.strip()
        if not line:
            pdf.ln(5)
        else:
            pdf.multi_cell(0, 8, line)

    pdf.output(filename)