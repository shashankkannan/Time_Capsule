from django.db import models
from TimeCapsuleManagement.models import Capsule


class SearchableCapsule(models.Model):
    capsule = models.OneToOneField(Capsule, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Searchable {self.capsule.name}"