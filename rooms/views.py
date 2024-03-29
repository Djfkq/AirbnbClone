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
from django.conf import settings
from medias.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
from django.utils import timezone


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
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

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


class RoomDetail(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

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
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
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
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", "1").replace("/", "")
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = page_size * (page - 1)
        end = start + page_size

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print("valid")
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            # review = serializer.save()
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            print("error!")
            return Response(serializer.errors)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DeosNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1).replace("/", "")
            int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = page_size * (page - 1)
        end = start + page_size

        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):
    permissions_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        month = request.query_params.get("month", "").replace("/", "")
        now = timezone.localtime(timezone.now()).date()

        bookings = Booking.objects.filter(room=room,
                                          kind=Booking.BookingKindChoices.ROOM,
                                          check_in__gt=now)
        # bookings = Booking.objects.filter(room__pk=pk)  #pk로 한번에 확인가능
        if month != "":
            bookings = bookings.filter(check_in__month=month)

        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"status":"ok"})
        else:
            return Response(serializer.errors)
