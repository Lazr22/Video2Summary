import re


def normalize_spaces(text: str) -> str:
    """
    Replace multiple spaces with a single space.
    """
    return re.sub(r"\s+", " ", text)


def fix_punctuation_spacing(text: str) -> str:
    """
    Fix spacing around punctuation.
    """
    # Remove space before punctuation
    text = re.sub(r"\s+([.,!?])", r"\1", text)

    # Ensure space after punctuation
    text = re.sub(r"([.,!?])([^\s])", r"\1 \2", text)

    return text


def capitalize_sentences(text: str) -> str:
    """
    Capitalize the first letter of each sentence.
    """
    sentences = re.split(r"([.!?])", text)
    result = ""

    for i in range(0, len(sentences), 2):
        sentence = sentences[i].strip()
        if sentence:
            sentence = sentence.capitalize()

        if i + 1 < len(sentences):
            punctuation = sentences[i + 1]
            result += sentence + punctuation + " "
        else:
            result += sentence

    return result.strip()


def clean_text(text: str) -> str:
    """
    Main cleaning pipeline.
    """
    text = text.strip()
    text = normalize_spaces(text)
    text = fix_punctuation_spacing(text)
    text = capitalize_sentences(text)

    return text