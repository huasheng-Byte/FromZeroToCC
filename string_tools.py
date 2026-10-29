import re


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


if __name__ == "__main__":
    print(slugify("Hello, World!"))
    print(slugify("  My  Fancy --Title  "))
