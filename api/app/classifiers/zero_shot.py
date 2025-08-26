from typing import Any, Dict, List, Optional

import torch
from gliclass import GLiClassModel, ZeroShotClassificationPipeline
from transformers import AutoTokenizer

from app.classifiers.classifier_base import ClassifierBase
from app.config.settings import settings


class ZeroShotClassifier(ClassifierBase):
    """
    Zero-shot classifier using GLiClass models for medical text classification.
    
    This classifier uses the GLiClass model which is specifically designed for
    zero-shot classification tasks, particularly effective for medical and
    scientific text classification.
    
    Example:
        classifier = ZeroShotClassifier()
        result = classifier.predict(
            "Medical text about neurological disorders",
            candidate_labels=["cardiovascular", "neurological", "hepatorenal", "oncological"]
        )
    """
    
    def __init__(
        self,
        model_name: str = "knowledgator/gliclass-modern-large-v2.0",
        device: Optional[str] = None,
        classification_type: str = "multi-label",
        threshold: float = 0.9,
        **kwargs
    ):
        """
        Initialize the zero-shot classifier.
        
        Args:
            model_name: Name of the pre-trained GLiClass model to use
            device: Device to run inference on ('cuda:0', 'cpu', or None for auto)
            classification_type: Type of classification ('multi-label' or 'single-label')
            threshold: Confidence threshold for multi-label classification
            **kwargs: Additional arguments passed to ClassifierBase
        """
        self.model_name = model_name
        # Force CPU for now to avoid MPS issues
        self.device = "cpu"
        self.classification_type = classification_type
        self.threshold = threshold
        self.pipeline = None
        self.tokenizer = None
        self.model = None
        
        # Initialize base class
        super().__init__(**kwargs)

        self.load_model()
        
    
    def load_model(self) -> bool:
        """
        Load the GLiClass zero-shot classification pipeline.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            self.logger.info(f"Loading GLiClass model: {self.model_name}")
            self.logger.info(f"Using device: {self.device}")
            self.logger.info(f"Classification type: {self.classification_type}")
            
            # Load model and tokenizer
            self.model = GLiClassModel.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, 
                add_prefix_space=True
            )
            
            # Create the zero-shot pipeline
            self.pipeline = ZeroShotClassificationPipeline(
                self.model, 
                self.tokenizer, 
                classification_type=self.classification_type, 
                device=self.device
            )
            
            self.is_loaded = True
            self.logger.info("GLiClass model loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load GLiClass model: {str(e)}")
            self.is_loaded = False
            return False
    
    def predict(
        self,
        content: dict[str, str],
        candidate_labels: Optional[List[str]] = None,
        threshold: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform zero-shot classification on a single text.
        
        Args:
            text: Input text to classify
            candidate_labels: List of possible labels to choose from
            threshold: Confidence threshold for multi-label classification
            **kwargs: Additional arguments
            
        Returns:
            Dict containing prediction results
        """
        if not self.is_model_ready():
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        
        # Use threshold from instance if not provided
        if threshold is None:
            threshold = self.threshold
        
        # Preprocess text
        processed_text = self.preprocess_text(content)
        
        
        try:
            # Run zero-shot classification
            results = self.pipeline(processed_text, settings.labels, threshold=threshold)
            
            # Extract results (pipeline returns list, we take first element for single text)
            result = results[0] if results else []

            # Format the result
            prediction = {
                "label": result[0]["label"] if result else None,
                "confidence": result[0]["score"] if result else 0.0,
                "probabilities": {item["label"]: item["score"] for item in result},
                "metadata": {
                    "model_name": self.model_name,
                    "classification_type": self.classification_type,
                    "threshold": threshold,
                    "candidate_labels": candidate_labels,
                    "total_predictions": len(result)
                }
            }
            
            # Add multi-label results if applicable
            if self.classification_type == "multi-label":
                prediction["labels"] = [item["label"] for item in result]
                prediction["confidences"] = [item["score"] for item in result]
                prediction["above_threshold"] = len(result)

            self.logger.info(f"Prediction: {prediction}")
            
            return prediction
            
        except Exception as e:
            self.logger.error(f"Prediction failed: {str(e)}")
            raise RuntimeError(f"Prediction failed: {str(e)}")
    
    def predict_batch(
        self,
        texts: List[str],
        candidate_labels: Optional[List[str]] = None,
        threshold: Optional[float] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Perform zero-shot classification on multiple texts.
        
        Args:
            texts: List of input texts to classify
            candidate_labels: List of possible labels to choose from
            threshold: Confidence threshold for multi-label classification
            **kwargs: Additional arguments
            
        Returns:
            List of prediction results, one per input text
        """
        if not self.is_model_ready():
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        if not texts:
            return []
        
        results = []
        for text in texts:
            try:
                result = self.predict(
                    text,
                    candidate_labels=candidate_labels,
                    threshold=threshold
                )
                results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to classify text '{text[:50]}...': {str(e)}")
                # Add error result
                results.append({
                    "label": None,
                    "confidence": 0.0,
                    "probabilities": {},
                    "metadata": {"error": str(e)},
                    "text": text
                })
        
        return results
    
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get detailed information about the GLiClass model.
        
        Returns:
            Dict containing model information
        """
        base_info = super().get_model_info()
        base_info.update({
            "model_name": self.model_name,
            "device": self.device,
            "model_type": "gliclass-zero-shot-classification",
            "classification_type": self.classification_type,
            "threshold": self.threshold,
            "supports_multi_label": True,
            "library": "gliclass"
        })
        return base_info
