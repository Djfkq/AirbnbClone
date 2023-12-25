from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    """
    print(model_admin)
    print(dir(request))
    print(request.user)
    print(dir(request.user))
    print(rooms)
    """
    for room in rooms.all():  # rooms : 선택된 개체들
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices, )

    list_display = (
        'name',
        'price',
        'kind',
        'total_amenities',
        'rating',
        'owner',
        "created_at",
    )
    list_filter = (
        'country',
        'city',
        'price',
        'rooms',
        'toilets',
        'pet_friendly',
        'kind',
        'amenities',
        "created_at",
        "updated_at",
    )

    ########################################
    ## 두번째 방법 : 관리자 패널만을 위한 메소드로 설정
    # def total_amenities(self, room):
    #     # print(room)
    #     return room.amenities.count()

    ########################################
    search_fields = (
        'name',  #'^name : startswith과 동일, =name:100% 일치값'
        'price',
        'owner__username'  #owner의 username으로 검색
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
