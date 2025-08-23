from typing import Dict, List
import pandas as pd
from schemas import ArticleRequest, ArticleResponse


class ClassificationService:
    """Service for article classification"""
    
    def __init__(self):
        # Mock labels for demonstration - in a real app, this would be a trained model
        self.available_labels = [
            "machine_learning", "deep_learning", "computer_vision", 
            "natural_language_processing", "data_science", "statistics",
            "optimization", "robotics", "cybersecurity", "bioinformatics"
        ]
    
    def classify_article(self, article: ArticleRequest) -> ArticleResponse:
        """
        Classify a single article based on title and abstract
        
        Args:
            article: ArticleRequest containing title and abstract
            
        Returns:
            ArticleResponse with title and predicted labels
        """
        # Mock classification logic - in a real app, this would use a trained model
        labels = self._mock_classification(article.title, article.abstract)
        
        return ArticleResponse(
            title=article.title,
            labels=list(labels.keys())  # Convert to list of label names
        )
    
    def classify_articles_batch(self, articles: List[ArticleRequest]) -> List[ArticleResponse]:
        """
        Classify multiple articles
        
        Args:
            articles: List of ArticleRequest objects
            
        Returns:
            List of ArticleResponse objects
        """
        return [self.classify_article(article) for article in articles]
    
    def _mock_classification(self, title: str, abstract: str) -> Dict[str, float]:
        """
        Mock classification logic - generates random confidence scores
        
        In a real application, this would:
        1. Preprocess the text (tokenization, cleaning, etc.)
        2. Use a trained model to predict labels
        3. Return confidence scores for each label
        """
        import random
        
        # Simple keyword-based mock classification
        text = (title + " " + abstract).lower()
        
        labels = {}
        for label in self.available_labels:
            # Mock confidence based on keyword presence
            if any(keyword in text for keyword in label.split('_')):
                confidence = random.uniform(0.6, 0.95)
            else:
                confidence = random.uniform(0.0, 0.3)
            
            # Only include labels with confidence > 0.1
            if confidence > 0.1:
                labels[label] = round(confidence, 3)
        
        # Ensure at least one label is returned
        if not labels:
            labels[self.available_labels[0]] = round(random.uniform(0.5, 0.8), 3)
        
        return labels
