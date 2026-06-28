import re

def clean_text(text: str) -> str:
    # remove extra spaces/newlines/tabs
    text = re.sub(r'\s+', ' ', text)

    # remove unwanted special characters
    text = re.sub(r'[^a-zA-Z0-9@.+#\-/ ]', '', text)

    # remove multiple spaces
    text = re.sub(r' +', ' ', text)

    # strip start/end spaces
    text = text.strip()
    return text



