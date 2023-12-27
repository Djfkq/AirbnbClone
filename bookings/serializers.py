from rest_framework.serializers import ModelSerializer
from .models import Booking


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class PrivateBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "kind",
            "check_in",
            "check_out",
            "guests",
        )

        def validate_check_in(self, value):
            print("validate_check_in")
            # print(value)
            return value
