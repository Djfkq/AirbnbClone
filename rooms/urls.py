from django.urls import path
from . import views

urlpatterns = [
    #######################################################################
    ## html templates 렌더링 연습
    # path('', views.see_all_rooms),
    # path('<int:room_id>', views.see_one_room),
    # path('<str:room_name>', views.see_room_name),
    # path('<int:room_id>/<str:room_name>', views.see_room_name2)
    #######################################################################
    #######################################################################
    path('amenities/', views.Amenities.as_view()),
    path('amenities/<int:pk>', views.AmenityDetail.as_view()),
    path('', views.Rooms.as_view()),
    path('<int:pk>', views.RoomDetail.as_view()),
    path('<int:pk>/reviews/', views.RoomReviews.as_view()),
    path('<int:pk>/amenities/', views.RoomAmenities.as_view()),
    path('<int:pk>/photos/', views.RoomPhotos.as_view()),
    path('<int:pk>/bookings/', views.RoomBookings.as_view()),
]
