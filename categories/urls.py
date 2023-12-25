from django.urls import path
from . import views

urlpatterns = [
    ############################################
    ## < rest_framework 원리 이해 >
    # path('', views.categories),
    # path('<int:pk>/', views.category),
    ############################################
    ############################################
    ## < 1차 리팩토링 및 2차 리팩토링에도 그대로 적용 가능>
    # path('', views.Categories.as_view()),
    # path('<int:pk>/', views.CategoryDetail.as_view()),
    ############################################
    ############################################
    ## < 3차 리팩토링 >
    path(
        '',
        views.CategoryViewSet.as_view({
            "get": "list",
            "post": "create",
        }, ),
    ),
    path(
        '<int:pk>/',  # 반드시 pk로 적어야함
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }, ),
    ),
    ############################################
]
