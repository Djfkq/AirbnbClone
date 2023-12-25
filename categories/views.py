from django.http import JsonResponse
from .models import Category
from django.core import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

#######################################################################################################################################

## < rest_framework 원리 이해 >

#######################################################################
## 1. rest_framework 사용 안했을 경우
# def categories(request):
#     all_categories = Category.objects.all()
#     ###########################################
#     # Object of type QuerySet is not JSON serializable : QuerySet은 JSON으로 변환안되서 오류남(Serializer 필요)
#     # return JsonResponse({
#     #     "ok": True,
#     #     "categories": all_categories,
#     # })
#     ###########################################
#     return JsonResponse({
#         "ok":
#         True,
#         "categories":
#         serializers.serialize("json", all_categories),
#     })
#######################################################################

#######################################################################
## 2. rest_framework 사용 했을 경우 : 이때에도 serializer가 없어서 오류남
# @api_view()
# def categories(request):
#     return Response({
#         "ok": True,
#         "categories": Category.objects.all(),
#     })
#######################################################################
#######################################################################
## 3. rest_framework와 serializer 사용시
# @api_view(["GET", "POST"])
# def categories(request):
#     if request.method == "GET":
#         all_categories = Category.objects.all()
#         # serializer = CategorySerializer(all_categories[0]) # many=True 없으면 하나의 객체만 넣을 수 있음
#         serializer = CategorySerializer(
#             all_categories,
#             many=True,
#         )  # many=True : 여러개의 객체를 가지고 을 때
#         return Response(serializer.data)
#     elif request.method == "POST":
#         # print(request.data)  # 사용자가 POST 요청한 데이터 값

#         #===================================================================
#         # 아래 처럼 바로 데이터 생성할 수 있지만, 데이터 유효성 검증이 안되서 오류 발생 가능성
#         # Category.objects.create(
#         #     name=request.data['name'],
#         #     kind=request.data['kind'],
#         # )
#         #===================================================================
#         #######################################################################
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             new_category = serializer.save(
#             )  # save()하면 serializers.py에서 create메서드를 찾기 시작함
#             return Response(CategorySerializer(new_category).data)
#         else:
#             return Response(serializer.errors)
#         #######################################################################

# @api_view(["GET", "PUT", "DELETE"])
# def category(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         raise NotFound

#     if request.method == "GET":
#         serializer = CategorySerializer(category)  #many=True 필요 없음
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CategorySerializer(
#             category,
#             data=request.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             updated_category = serializer.save(
#             )  # save()하면 serializers.py에서 update메서드를 찾기 시작함
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.errors)
#     elif request.method == "DELETE":
#       category.delete()
#       return Response(status=HTTP_204_NO_CONTENT)

## < rest_framework 원리 이해 >
#######################################################################################################################################

#######################################################################################################################################
## < 1차 리팩토링 및 2차 리팩토링에도 그대로 적용 가능>
# class Categories(APIView):
#     def get(self, request):
#         all_categories = Category.objects.all()
#         serializer = CategorySerializer(
#             all_categories,
#             many=True,
#         )
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             new_category = serializer.save()
#             return Response(CategorySerializer(new_category).data)
#         else:
#             return Response(serializer.errors)

# class CategoryDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             raise NotFound

#     def get(self, request, pk):
#         serializer = CategorySerializer(self.get_object(pk))  #many=True 필요 없음
#         print(serializer)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         serializer = CategorySerializer(
#             self.get_object(pk),
#             data=request.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             updated_category = serializer.save(
#             )  # save()하면 serializers.py에서 update메서드를 찾기 시작함
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.errors)

#     def delete(self, request, pk):
#         self.get_object(pk).delete()
#         return Response(status=HTTP_204_NO_CONTENT)
## < 1차 리팩토링 및 2차 리팩토링에도 그대로 적용 가능>
#######################################################################################################################################

#######################################################################################################################################
## < 3차 리팩토링 >
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
#######################################################################################################################################