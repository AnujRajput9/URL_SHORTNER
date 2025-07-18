from django.db import models

class ShortURL(models.Model):
    shortcode = models.CharField(max_length=10, unique=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    click_count = models.PositiveIntegerField(default=0)

class ClickAnalytics(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
