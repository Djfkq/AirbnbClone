from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price_per_night',
        'description',
        'address',
        'pets_allowed',
    )
    list_display_links = (
        "name",
        "address",
    )
    list_filter = (
        "price_per_night",
        "pets_allowed",
    )
    list_editable = (
        "price_per_night",
        "pets_allowed",
    )
    search_fields = ("address", )
    # search_fields = ("address__startswith", "address__endswith")
    # exclude = ("price_per_night", )
    fields = (
        "name",
        "address",
        (
            "price_per_night",
            "pets_allowed",
        ),
        "owner",
    )
