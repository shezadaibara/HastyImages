# from celery import shared_task
# from Utils.minioClient import MC
# from Gallery.models import Image, Gallery

# #@shared_task
# def get_image_metadata(file_id):
#     image_obj = Image.objects.get(file_id)
#     minIO = MC.getInstance()
#     data = minIO.client.stat_object(minIO.bucket_name, image_obj.path)
#     for k, v in data.metadata:
#         print(k, v)