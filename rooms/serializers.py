from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


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
            "is_owner",
            "photos",
        )

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        print(self.context)
        
        request = self.context["request"]
      
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(
        read_only=True)  # read_only=True : POST 요청시 owner에 대한 정보를 적지 않아도 됨
    amenities = AmenitySerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(read_only=True)

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    # review들을 한꺼번에 보여주기보단, 새로운 URL만듬
    # reviews = ReviewSerializer(
    #     many=True,
    #     read_only=True,
    # )

    class Meta:
        model = Room
        fields = "__all__"

    #####################
    # < serializer.py 에서 room = serializer.save(owner=request.user) 부분 확인용 >
    # def create(self, validated_data):
    #     print(validated_data)
    #     return

    #####################

    # 메서드 이름은 : get_속성이름으로 해야함, 두번째 인자는 해당하는 object
    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        # views에서 serializer부분에 context={} 보냈을 때 self.context로 접근 가능
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()
        
      
    



# class RoomSerializer(ModelSerializer):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         # depth = 1  # 개별 값들을 key값으로 표시하는 대신에 실제 값으로 표시
