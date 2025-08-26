from typing import Any, Dict, List, Optional, Union
import requests
import json
import logging

from app.classifiers.classifier_base import ClassifierBase
from app.classifiers.few_shot_prompts import get_few_shot_examples, create_classification_prompt, get_prompt_info
from app.config.settings import settings


class FewShotClassifier(ClassifierBase):
    """
    Few-shot classifier using Ollama with Llama 3.2:8b for medical text classification.
    
    This classifier uses few-shot prompting with examples from training data
    to classify medical articles into predefined categories.
    
    Example:
        classifier = FewShotClassifier()
        result = classifier.predict({
            "title": "Medical article title",
            "abstract": "Medical article abstract"
        })
    """
    
    def __init__(
        self,
        model_name: str = "llama3.1:8b",
        ollama_base_url: str = "http://ollama:11434",
        max_examples: int = 8,
        **kwargs
    ):
        """
        Initialize the few-shot classifier using Ollama.
        
        Args:
            model_name: Name of the Ollama model to use (default: llama3.2:8b)
            ollama_base_url: Base URL for Ollama API (default: http://localhost:11434)
            max_examples: Maximum number of few-shot examples to use (default: 8)
            **kwargs: Additional arguments passed to ClassifierBase
        """
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url
        self.max_examples = max_examples
        
        # Ollama API endpoint
        self.api_url = f"{ollama_base_url}/api/generate"
        
        # Few-shot examples
        self.few_shot_examples = []
        
        # Initialize base class
        super().__init__(**kwargs)
        
        # Load fixed few-shot examples
        self._load_few_shot_examples()
    
    def _load_few_shot_examples(self) -> None:
        """
        Load few-shot examples from the prompts file.
        """
        self.few_shot_examples = get_few_shot_examples()
        self.logger.info(f"Loaded {len(self.few_shot_examples)} few-shot examples from prompts file")
        
        # Log prompt information
        prompt_info = get_prompt_info()
        self.logger.info(f"Prompt info: {prompt_info['single_label_count']} single-label, {prompt_info['multi_label_count']} multi-label examples")
    
    def load_model(self) -> bool:
        """
        Check if Ollama is available and the model is accessible.
        
        Returns:
            bool: True if Ollama is accessible, False otherwise
        """
        try:
            self.logger.info(f"Checking Ollama availability at: {self.ollama_base_url}")
            
            # Test Ollama connection
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=10)
            if response.status_code != 200:
                self.logger.error(f"Ollama API not accessible: {response.status_code}")
                self.is_loaded = False
                return False
            
            # Check if the model is available
            models_response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=10)
            if models_response.status_code == 200:
                models = models_response.json().get('models', [])
                model_names = [model.get('name', '') for model in models]
                
                if self.model_name not in model_names:
                    self.logger.warning(f"Model {self.model_name} not found in Ollama. Available models: {model_names}")
                    self.logger.info("You may need to pull the model using: ollama pull llama3.2:8b")
                    # Don't fail here, as the model might be pulled later
                
                self.is_loaded = True
                self.logger.info(f"Ollama accessible. Model {self.model_name} status checked.")
                return True
            else:
                self.logger.error(f"Failed to get models from Ollama: {models_response.status_code}")
                self.is_loaded = False
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to connect to Ollama: {str(e)}")
            self.logger.error("Make sure Ollama is running and accessible at the specified URL")
            self.is_loaded = False
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error checking Ollama: {str(e)}")
            self.is_loaded = False
            return False
    
    def _create_prompt(self, text: str) -> str:
        """
        Create a few-shot prompt for classification using the prompts module.
        
        Args:
            text: Input text to classify
            
        Returns:
            Formatted prompt string
        """
        return create_classification_prompt(text, settings.labels, self.max_examples)
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API to generate text.
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            Generated text response
        """
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.95,
                    "max_tokens": 100
                }
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=300  # Increased timeout to 5 minutes for first inference
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                self.logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                raise RuntimeError(f"Ollama API returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request to Ollama failed: {str(e)}")
            raise RuntimeError(f"Failed to communicate with Ollama: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error calling Ollama: {str(e)}")
            raise RuntimeError(f"Error calling Ollama: {str(e)}")
    
    def predict(self, content: dict[str, str], **kwargs) -> Dict[str, Any]:
        """
        Perform classification prediction on a single text input.
        
        Args:
            text: Input text dict with 'title' and 'abstract' keys
            
        Returns:
            Dict containing prediction results
        """
        if not self.is_model_ready():
            # Try to load/check the model
            if not self.load_model():
                raise RuntimeError("Ollama not accessible. Make sure Ollama is running and the model is available.")
        
        # Preprocess text
        processed_text = self.preprocess_text(content)
        if not processed_text:
            return {
                'label': None,
                'confidence': 0.0,
                'probabilities': {},
                'metadata': {'error': 'Empty or invalid text'}
            }
        
        try:
            # Create prompt
            prompt = self._create_prompt(processed_text)
            
            # Generate response using Ollama
            response_text = self._call_ollama(prompt)
            
            # Parse the response to get the predicted label
            predicted_label = self._parse_response(response_text)

            print(f"Predicted label: {predicted_label}")
            
            # For now, return basic structure - confidence scoring would need more sophisticated parsing
            return {
                'labels': predicted_label.split("|"),
                'confidence': 0.8,  # Placeholder - would need proper confidence calculation
                'probabilities': {predicted_label: 0.8} if predicted_label else {},
                'metadata': {
                    'prompt': prompt,
                    'response': response_text,
                    'model': self.model_name,
                    'ollama_url': self.ollama_base_url,
                    'few_shot_examples_used': len(self.few_shot_examples[:self.max_examples])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Prediction failed: {str(e)}")
            return {
                'label': None,
                'confidence': 0.0,
                'probabilities': {},
                'metadata': {'error': str(e)}
            }
    
    def predict_batch(self, texts: List[dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Perform classification prediction on multiple text inputs.
        
        Args:
            texts: List of input text dicts with 'title' and 'abstract' keys
            
        Returns:
            List of prediction results, one dict per input text
        """
        return [self.predict(text) for text in texts]
    
    def get_available_labels(self) -> List[str]:
        """
        Get the list of available classification labels.
        
        Returns:
            List of possible class labels
        """
        return settings.labels
    
    def _parse_response(self, response: str) -> Optional[str]:
        """
        Parse the model response to extract the predicted label.
        
        Args:
            response: Raw response from the model
            
        Returns:
            Predicted label or None if parsing fails
        """
        # Clean the response
        response = response.strip().lower()
        
        # Try to find a matching label
        for label in settings.labels:
            if label.lower() in response:
                return label
        
        # If no exact match, try partial matching
        for label in settings.labels:
            if any(word in response for word in label.lower().split()):
                return label
        
        return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dict containing model information
        """
        base_info = super().get_model_info()
        base_info.update({
            'model_name': self.model_name,
            'ollama_base_url': self.ollama_base_url,
            'max_examples': self.max_examples,
            'few_shot_examples_count': len(self.few_shot_examples),
            'prompt_info': get_prompt_info()
        })
        return base_info

    
