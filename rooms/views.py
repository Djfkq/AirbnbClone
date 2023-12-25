#######################################################################################
## html templates 렌더링 연습

# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import Room
#
#
# def see_all_rooms(request):
#     rooms = Room.objects.all()
#     return render(
#         request,
#         "all_rooms.html",
#         {
#             "rooms": rooms,
#             "title": "Hello! this title comes from django!",
#         },
#     )

# def see_one_room(request, room_id):
#     try:
#         room = Room.objects.get(id=room_id)
#         return render(
#             request,
#             "room_detail.html",
#             {
#                 "room": room,
#             },
#         )
#     except Room.DoesNotExist:
#         return render(
#             request,
#             "room_detail.html",
#             {
#                 "not_found": True,
#             },
#         )

# def see_room_name(request, room_name):
#     return HttpResponse(f"see rooms with name: {room_name}")

# def see_room_name2(request, room_id, room_name):
#     return HttpResponse(f"see rooms with id: {room_id} and name: {room_name}")
# #######################################################################################

#######################################################################################
from rest_framework.views import APIView
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from django.db import transaction
from reviews.serializers import ReviewSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        # print(dir(request.user))
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                # print(request.data)
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                ###############################################################
                # room = serializer.save(
                #     owner=request.user,
                #     category=category,
                # )  # serializers.py에서 create 메서드의 validated_data argument에 owner:request.user가 추가됨
                # amenities = request.data.get('amenities')
                # for amenity_pk in amenities:
                #     try:
                #         amenity = Amenity.objects.get(pk=amenity_pk)
                #     except Amenity.DoesNotExist:
                #         room.delete()
                #         raise ParseError(
                #             f"Amenity with id {amenity_pk} not found")
                #     room.amenities.add(amenity)
                # serializer = RoomDetailSerializer(room)
                # return Response(serializer.data)
                ###############################################################
                ###############################################################
                try:
                    ## transaction : 에러가 발생하면 DB에 변경사항 반영안함
                    with transaction.atomic():
                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )  # serializers.py에서 create 메서드의 validated_data argument에 owner:request.user가 추가됨
                        amenities = request.data.get('amenities')
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
                    ###############################################################
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={
                "request": request,
            },  # context={} 입력하면 serializers.py에서 self.context로 접근가능!
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            with transaction.atomic():
                category_pk = request.data.get('category')
                amenities_pk = request.data.get('amenities')

                if category_pk:
                    try:
                        category = Category.objects.get(pk=category_pk)
                    except Exception:
                        raise ParseError("Category not found")
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The Category kind sholud be 'rooms'")
                else:
                    category = room.category

                if amenities_pk:
                    amenities = []
                    for amenity_pk in amenities_pk:
                        try:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            amenities.append(amenity)
                        except Exception:
                            raise ParseError("Amenitiy not found")
                else:
                    amenities = room.amenities.all()

                updated_room = serializer.save(
                    owner=request.user,
                    category=category,
                    amenities=amenities,
                )
                return Response(RoomDetailSerializer(updated_room).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1).replace("/", "")
            page = int(page)
        except ValueError:
            page = 1

        page_size = 3
        start = page_size * (page - 1)
        end = start + page_size

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)
