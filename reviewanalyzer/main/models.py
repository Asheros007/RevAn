from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AnalysisResult(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]
    
    # Basic info
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    review_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    # Overview data
    overall_sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    sentiment_score = models.FloatField()
    
    # Word counts
    total_words = models.IntegerField()
    positive_words = models.IntegerField()
    negative_words = models.IntegerField()
    neutral_words = models.IntegerField()
    intensifiers = models.IntegerField()
    negations = models.IntegerField()
    
    # Percentages
    positive_percentage = models.FloatField()
    negative_percentage = models.FloatField()
    neutral_percentage = models.FloatField()
    
    # Summary data
    positive_summary = models.JSONField(default=list) 
    negative_summary = models.JSONField(default=list) 
    neutral_summary = models.JSONField(default=list) 
    
    # Word analysis
    positive_words_list = models.JSONField(default=list)
    negative_words_list = models.JSONField(default=list) 
    neutral_words_list = models.JSONField(default=list) 
    intensifiers_list = models.JSONField(default=list) 
    negations_list = models.JSONField(default=list) 
    
    class Meta:
        db_table = 'analysis_results'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['overall_sentiment']),
        ]
    
    def __str__(self):
        return f"{self.product_name} - {self.overall_sentiment} ({self.created_at.date()})"