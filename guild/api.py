# from django.core.exceptions import ObjectDoesNotExist
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from . import models, serializers
#
#
# class GetFilePath(APIView):
#     @staticmethod
#     def get(request):
#         code = request.GET.get('code')
#         try:
#             file = models.Post.objects.get(code=code)
#             file.increment_download_count()
#             serialized_data = serializers.FileModelSerializer(file)
#             return Response(serialized_data.data)
#         except ObjectDoesNotExist:
#             return Response(None, status=404)
