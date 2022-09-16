from typing import List
from transformers import pipeline


def classify_text(text: str, categories: List[str]) -> List[str]:
    classifier = pipeline(
        "zero-shot-classification", model="typeform/distilbert-base-uncased-mnli"
    )
    sequence_to_classify = text
    candidate_labels = categories

    res = classifier(sequence_to_classify, candidate_labels)

    return dict(zip(res["labels"], res["scores"]))
