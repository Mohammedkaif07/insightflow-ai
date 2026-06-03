import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text by removing messy spacing,
    repeated dots, unnecessary blank lines, and table-of-content noise.
    """

    if not text:
        return ""

    # Remove repeated dots from table of contents
    text = re.sub(r"\.{5,}", " ", text)

    # Replace tabs and multiple spaces with single space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces before punctuation
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)

    # Replace 3+ newlines with only 2 newlines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading/trailing spaces on each line
    lines = [line.strip() for line in text.splitlines()]

    # Remove empty repeated lines
    cleaned_lines = []
    for line in lines:
        if line:
            cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)

    return cleaned_text.strip()