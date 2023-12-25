from django.db import models
from common.models import CommonModel


class Room(CommonModel):
    """Room model Definition"""
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire_place")
        PRIVATE_ROOM = ("private_room", "Private_room")
        SHARED_ROOM = ("shared_room", "Shared_room")

    name = models.CharField(max_length=180, default="")
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250, )
    pet_friendly = models.BooleanField(default=True, )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )
    category = models.ForeignKey(
        'categories.Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self):
        return self.name

    ########################################
    ## 1.첫번째는 model에 입력하는 방법이고 두번째는 admin에 입력하는 방법
    def total_amenities(self):
        # print(self.amenities.all())
        return self.amenities.count()

    ########################################

    def rating(self):

        count = self.reviews.count()
        if count == 0:
            return "No Reviews"
        else:
            ########################################################
            # total_rating = 0
            # for review in self.reviews.all():
            #     total_rating += review.rating
            # return round(total_rating / count, 2)
            ########################################################
            ########################################################
            total_rating = 0
            # values("rating") 안하면 rating말고 다른 모든 변수들 다 가지고와서 느림
            # self.reviews.all().values("rating") : [{'rating':5} {'rating':3}, {'rating':4}]
            for rating in self.reviews.all().values("rating"):
                total_rating += rating["rating"]
            return round(total_rating / count, 2)
            ########################################################
            ########################################################
            # return self.reviews.aggregate(models.Avg('rating'))['rating__avg']
            ########################################################


class Amenity(CommonModel):
    """Amenity model Definition"""
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
