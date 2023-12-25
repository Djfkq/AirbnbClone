from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = 'Filter by words!'
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),  # (url표시, 관리자페이지표시)
            ("great", "Great"),
            ("awsome", "Awsome"),
        ]

    def queryset(self, request, reviews):
        # print(dir(request))
        # print(request.GET)  # url에 있는 값 들고오는것
        word = self.value()  # 바로 값 들고오기
        if word is not None:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


class ReviewRatingFilter(admin.SimpleListFilter):
    title = 'Filter by Rating'
    parameter_name = "ReviewRating"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, reviews):
        rating = self.value()
        if rating is not None:
            if rating == "good":
                return reviews.filter(rating__gte=3)
            else:
                return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        ReviewRatingFilter,
        "rating",
        "user__is_host",
        "room__category",  # room__category__name : 예를들어서 ForeignKey 두개 이상도 가능(name은 그냥 예시로 적은거)
        "room__pet_friendly",
    )
