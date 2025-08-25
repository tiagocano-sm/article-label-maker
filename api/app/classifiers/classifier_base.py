from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ClassifierBase(ABC):
    """
    Abstract base class for AI model-based classifiers.
    
    This class defines the interface for classifiers that use pre-trained AI models
    for inference. It does not include training functionality as that can be
    handled separately in other files.
    
    Subclasses should implement the abstract methods to provide specific
    classification logic for different types of AI models.
    """
    
    def __init__(self, model_path: Optional[Union[str, Path]] = None, **kwargs):
        """
        Initialize the classifier.
        
        Args:
            model_path: Path to the pre-trained model file or directory
            **kwargs: Additional configuration parameters
        """
        self.model_path = Path(model_path) if model_path else None
        self.model = None
        self.is_loaded = False
        self.config = kwargs
        
        # Initialize logging
        self.logger = logger.getChild(self.__class__.__name__)

    
    @abstractmethod
    def load_model(self) -> bool:
        """
        Load the AI model from the specified path.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Perform classification prediction on a single text input.
        
        Args:
            text: Input text to classify
            
        Returns:
            Dict containing prediction results with keys like:
            - 'label': predicted class label
            - 'confidence': confidence score (0.0 to 1.0)
            - 'probabilities': dict of class probabilities
            - 'metadata': additional prediction information
        """
        pass
    
    @abstractmethod
    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Perform classification prediction on multiple text inputs.
        
        Args:
            texts: List of input texts to classify
            
        Returns:
            List of prediction results, one dict per input text
        """
        pass
    
    @abstractmethod
    def get_available_labels(self) -> List[str]:
        """
        Get the list of available classification labels.
        
        Returns:
            List of possible class labels
        """
        pass
    
    def is_model_ready(self) -> bool:
        """
        Check if the model is loaded and ready for inference.
        
        Returns:
            bool: True if model is ready, False otherwise
        """
        return self.is_loaded and self.model is not None
    
    def preprocess_text(self, text: dict[str, str]) -> str:
        """
        Preprocess input text before classification.
        
        This is a default implementation that can be overridden by subclasses
        for specific preprocessing needs.
        
        Args:
            text: Raw input text
            
        Returns:
            Preprocessed text
        """
        if not text["abstract"]:
            return ""
        
        # Basic preprocessing: strip whitespace and normalize and join title and abstract
        text = text["title"] + "\n" + text["abstract"]
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        return text
    
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dict containing model information
        """
        return {
            "model_path": str(self.model_path) if self.model_path else None,
            "is_loaded": self.is_loaded,
            "model_type": self.__class__.__name__,
            "available_labels": self.get_available_labels() if self.is_model_ready() else [],
            "config": self.config
        }
    
    def __enter__(self):
        """Context manager entry."""
        if not self.is_model_ready():
            self.load_model()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        # Cleanup if needed
        pass
    
    def __repr__(self) -> str:
        """String representation of the classifier."""
        return f"{self.__class__.__name__}(model_path={self.model_path}, loaded={self.is_loaded})"
