from rest_framework import serializers
from .models import Category

#######################################################################################################################################
## < rest_framework 원리 이해  & 1차 리팩토링>
# class CategorySerializer(serializers.Serializer):
#     ## JSON으로 보여줄 정보를 적음
#     pk = serializers.IntegerField(
#         read_only=True)  # read_only=True : POST요청시 유저가 값을 안넣어도 삳관없도록 설정
#     # pk = serializers.CharField() # 출력 형태도 정할 수 있음
#     name = serializers.CharField(
#         required=True,
#         max_length=50,
#     )  # max_length=50은 POST 요청시 데이터 검증에 도움
#     kind = serializers.ChoiceField(
#         choices=Category.CategoryKindChoices.choices, )
#     created_at = serializers.DateTimeField(
#         read_only=True)  # read_only=True : POST요청시 유저가 값을 안넣어도 삳관없도록 설정

#     def create(self, validated_data):
#         # print(validated_data)
#         """
#         # 아래처럼 하면 비효율
#         Category.objects.create(
#           name = validated_data['name'],
#           kind = validated_data['kind'],
#         )
#         """
#         return Category.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#       if validated_data['name']:
#         instance.name = validated_data['name']
#       """
#         instance.name = validated_data.get('name', instance.name)
#         instance.kind = validated_data.get('kind', instance.kind)
#         instance.save()
#         return instance


## < rest_framework 원리 이해  & 1차 리팩토링>
#######################################################################################################################################
#######################################################################################################################################
## < 2차 리팩토링 & 3차 리팩토링>
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        ###########################
        # fields = "__all__"
        ###########################
        ###########################
        fields = (
            "name",
            "kind",
        )
        ###########################
        ###########################
        # exclude = ("created_at", )
        ###########################


## < 2차 리팩토링>
#######################################################################################################################################
