import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text by removing extra spaces,
    blank lines, and messy formatting.
    """

    if not text:
        return ""

    # Replace multiple spaces with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace multiple new lines with two new lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text