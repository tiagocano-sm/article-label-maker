from .zero_shot import ZeroShotClassifier

__all__ = ["ZeroShotClassifier"]

CLASSIFIER_TYPES = {
    "zero_shot": ZeroShotClassifier
}


def get_classifier(classifier_type: str):
    if classifier_type in CLASSIFIER_TYPES:
        return CLASSIFIER_TYPES[classifier_type]()
    else:
        raise ValueError(f"Invalid classifier type: {classifier_type}")

