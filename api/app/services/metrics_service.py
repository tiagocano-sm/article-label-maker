import numpy as np
from typing import Dict, List, Any
import json
import os
from datetime import datetime, timedelta

class MetricsService:
    def __init__(self):
        self.metrics_file = "metrics_data.json"
        self.labels = [
            "Machine Learning", "Deep Learning", "Computer Vision", 
            "Natural Language Processing", "Data Science", "Artificial Intelligence",
            "Robotics", "Neural Networks", "Big Data", "Cloud Computing"
        ]
        self._load_or_initialize_metrics()
    
    def _load_or_initialize_metrics(self):
        """Load existing metrics or initialize with mock data"""
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    self.metrics_data = json.load(f)
            except:
                self._initialize_mock_metrics()
        else:
            self._initialize_mock_metrics()
    
    def _initialize_mock_metrics(self):
        """Initialize with realistic mock metrics"""
        np.random.seed(42)  # For reproducible mock data
        
        # Generate mock data for overall confusion matrix
        total_samples = np.random.randint(1000, 5000)
        correct_predictions = int(total_samples * np.random.uniform(0.75, 0.95))  # 75-95% accuracy
        incorrect_predictions = total_samples - correct_predictions
        
        # Split incorrect predictions into different types
        false_positives = int(incorrect_predictions * np.random.uniform(0.3, 0.7))
        false_negatives = incorrect_predictions - false_positives
        
        # Generate overall confusion matrix
        overall_confusion_matrix = {
            "correct_predictions": correct_predictions,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "total_predictions": total_samples,
            "accuracy": round(correct_predictions / total_samples, 4)
        }
        
        # Calculate overall metrics
        overall_accuracy = overall_confusion_matrix["accuracy"]
        micro_f1 = np.random.uniform(0.7, 0.9)  # Realistic F1 score
        precision = np.random.uniform(0.75, 0.92)  # Realistic precision
        
        overall_metrics = {
            "micro_f1_score": round(micro_f1, 4),
            "precision": round(precision, 4),
            "overall_accuracy": overall_accuracy,
            "total_samples": total_samples,
            "correct_predictions": correct_predictions,
            "incorrect_predictions": incorrect_predictions
        }
        
        self.metrics_data = {
            "last_updated": datetime.now().isoformat(),
            "overall_metrics": overall_metrics,
            "overall_confusion_matrix": overall_confusion_matrix,
            "labels": self.labels,
            "has_data": True
        }
        
        self._save_metrics()
    
    def _save_metrics(self):
        """Save metrics to file"""
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics_data, f, indent=2)
    
    def update_metrics_from_predictions(self, y_true: List[List[str]], y_pred: List[List[str]]):
        """
        Update metrics with real predictions (to be used when real model is available)
        
        Args:
            y_true: List of true label lists for each sample
            y_pred: List of predicted label lists for each sample
        """
        # This method will be implemented when real model is available
        # For now, it just updates the timestamp
        self.metrics_data["last_updated"] = datetime.now().isoformat()
        self._save_metrics()
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all metrics data for dashboard"""
        return self.metrics_data
    
    def get_overall_metrics(self) -> Dict[str, Any]:
        """Get overall metrics only"""
        return self.metrics_data.get("overall_metrics", {})
    

    
    def get_overall_confusion_matrix(self) -> Dict[str, Any]:
        """Get overall confusion matrix"""
        return self.metrics_data.get("overall_confusion_matrix", {})
    
    def get_labels(self) -> List[str]:
        """Get list of all labels"""
        return self.metrics_data.get("labels", [])
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of key metrics for quick display"""
        overall = self.metrics_data.get("overall_metrics", {})
        return {
            "micro_f1_score": overall.get("micro_f1_score", 0),
            "macro_f1_score": overall.get("macro_f1_score", 0),
            "overall_accuracy": overall.get("overall_accuracy", 0),
            "total_samples": overall.get("total_samples", 0),
            "last_updated": self.metrics_data.get("last_updated", ""),
            "num_labels": len(self.metrics_data.get("labels", []))
        } 
