from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
        )

    rating = SerializerMethodField()
    def get_rating(self, room):
      return room.rating()

class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(
        read_only=True)  # read_only=True : POST 요청시 owner에 대한 정보를 적지 않아도 됨
    amenities = AmenitySerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(read_only=True)

    rating = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    #####################
    # < serializer.py 에서 room = serializer.save(owner=request.user) 부분 확인용 >
    # def create(self, validated_data):
    #     print(validated_data)
    #     return

    #####################

    def get_rating(self, room):  # 메서드 이름은 : get_속성이름으로 해야함, 두번째 인자는 해당하는 object
      return room.rating()


# class RoomSerializer(ModelSerializer):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         # depth = 1  # 개별 값들을 key값으로 표시하는 대신에 실제 값으로 표시
