from .zero_shot import ZeroShotClassifier
from .few_shot_prompting import FewShotClassifier

__all__ = ["ZeroShotClassifier", "FewShotClassifier"]

CLASSIFIER_TYPES = {
    "zero_shot": ZeroShotClassifier,
    "few_shot": FewShotClassifier
}


def get_classifier(classifier_type: str):
    if classifier_type in CLASSIFIER_TYPES:
        return CLASSIFIER_TYPES[classifier_type]
    else:
        raise ValueError(f"Invalid classifier type: {classifier_type}")

