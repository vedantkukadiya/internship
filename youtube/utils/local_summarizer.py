import re
from collections import Counter

STOP_WORDS = {
    "the", "is", "in", "and", "to", "of", "a", "for", "on", "that", "this",
    "it", "with", "as", "are", "was", "were", "be", "by", "an", "or", "at",
    "from", "but", "if", "then", "than", "so", "such", "into", "their",
    "there", "about", "can", "will", "just", "have", "has", "had", "you",
    "your", "they", "them", "he", "she", "his", "her", "we", "our", "i"
}


def split_sentences(text: str):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def summarize_text(text: str, max_sentences: int = 5) -> str:
    if not text or text.startswith("Error:"):
        return text

    text = re.sub(r"\s+", " ", text).strip()
    sentences = split_sentences(text)

    if not sentences:
        return "No summary available."

    if len(sentences) <= max_sentences:
        return "\n".join(f"- {sentence}" for sentence in sentences)

    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
    word_freq = Counter(
        word for word in words
        if word not in STOP_WORDS and len(word) > 2
    )

    if not word_freq:
        return "\n".join(f"- {sentence}" for sentence in sentences[:max_sentences])

    scored_sentences = []

    for index, sentence in enumerate(sentences):
        sentence_words = re.findall(r"\b[a-zA-Z']+\b", sentence.lower())

        if not sentence_words:
            continue

        score = sum(word_freq.get(word, 0) for word in sentence_words) / len(sentence_words)
        scored_sentences.append((score, index, sentence))

    top_sentences = sorted(scored_sentences, key=lambda x: x[0], reverse=True)[:max_sentences]
    top_sentences = sorted(top_sentences, key=lambda x: x[1])

    return "\n".join(f"- {sentence}" for _, _, sentence in top_sentences)