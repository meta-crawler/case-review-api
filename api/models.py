from django.db import models
from account.models import UserData


# Create your models here.
class AlertType(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name


class Alert(models.Model):
    alert_type = models.ForeignKey(AlertType, on_delete=models.CASCADE, null=True)
    zone = models.CharField(null=True, blank=True, max_length=255)
    camera = models.CharField(null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CaseStatus(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name


class CaseReviewStatus(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name


class CaseReview(models.Model):
    authority = models.ForeignKey(UserData, on_delete=models.CASCADE, null=True, related_name='authored_reviews')
    assigner = models.ForeignKey(UserData, on_delete=models.CASCADE, null=True, related_name='assigned_reviews')
    status = models.ForeignKey(CaseReviewStatus, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Case(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, null=True)
    authority = models.ForeignKey(UserData, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(CaseStatus, on_delete=models.CASCADE, null=True)
    case_review = models.ForeignKey(CaseReview, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    author = models.ForeignKey(UserData, on_delete=models.CASCADE, null=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True)
    comment = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
