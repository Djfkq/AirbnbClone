from django.db import models


class House(models.Model):
    """Model Definition for House"""
    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField(
        verbose_name="price", help_text="Positive Numbers Only")
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(
        default=True,
        null=False,
        help_text="Does this house allow pets?",
        verbose_name="Pets Allowed??",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,  #models.SET_NULL
    )

    def __str__(self):
        return self.name
