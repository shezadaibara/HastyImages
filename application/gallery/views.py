from django.shortcuts import render

# Create your views here.
import base64
import hashlib
import hmac
import os
import time
import json
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import Gallery, Image
from .serializers import ImageSerializer
from Utils.minioClient import MC
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from invitation.customAuthentication import MyCustomAuthentication
from django.utils import timezone


class ImagesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving Images.
    """
    authentication_classes = [MyCustomAuthentication]
    queryset = Image.objects.all().order_by('-updated')

    def list(self, request):
        token = request.GET.get('access_token')
        queryset = Image.objects.filter(token=token).order_by('-updated')
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        token = request.GET.get('access_token')
        queryset = Image.objects.filter(token=token).order_by('-updated')
        image = get_object_or_404(queryset, pk=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)


class FileUploadCompleteHandler(APIView):
    authentication_classes = [MyCustomAuthentication]
    def post(self, request, *args, **kwargs):
        file_id = request.POST.get('file')
        size = request.POST.get('fileSize')
        type_ = request.POST.get('fileType')
        meta_data = json.loads(request.POST.get('meta_data', "{}")) 
        data = {}
        if file_id:
            obj = Image.objects.get(id=int(file_id))
            obj.size = int(size)
            obj.uploaded = True
            obj.file_type = type_
            obj.updated = timezone.now()
            for k, v in meta_data.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
            obj.save()
            data['id'] = obj.id
            data['saved'] = True
        return Response(data, status=status.HTTP_200_OK)


class FilePolicyAPI(APIView):
    """
    This view is to get the AWS Upload Policy for our s3 bucket.
    What we do here is first create a FileItem object instance in our
    Django backend. This is to include the FileItem instance in the path
    we will use within our bucket as you'll see below.
    """
    authentication_classes = [MyCustomAuthentication]
    def post(self, request, *args, **kwargs):
        """
        The initial post request includes the filename
        and auth credientails. In our case, we'll use
        Session Authentication but any auth should work.
        """
        token = request.GET.get("access_token")
        if not token:
            return Response({"message": "access_token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        filename_req = request.data.get('filename')
        if not filename_req:
                return Response({"message": "A filename is required"}, status=status.HTTP_400_BAD_REQUEST)
        policy_expires = int(time.time()+5000)
        """
        Below we create the Django object. We'll use this
        in our upload path to AWS. 

        Example:
        To-be-uploaded file's name: Some Random File.jpg
        Eventual Path on S3: <bucket>/username/2312/2312.jpg
        """
        gallery_name = timezone.now().strftime("%Y-%m-%d")
        gallery_obj, _ = Gallery.objects.get_or_create(name=gallery_name, token=token)
        file_obj = Image.objects.create(gallery=gallery_obj, name=filename_req, token=token)
        
        file_obj_id = file_obj.id
        upload_start_path = "{token}/{gallery}/{file_obj_id}/".format(
                    token = token,
                    gallery = gallery_name,
                    file_obj_id=file_obj_id
            )
        _, file_extension = os.path.splitext(filename_req)
        filename_final = "{file_obj_id}{file_extension}".format(
                    file_obj_id= file_obj_id,
                    file_extension=file_extension

                )
        """
        Eventual file_upload_path includes the renamed file to the 
        Django-stored FileItem instance ID. Renaming the file is 
        done to prevent issues with user generated formatted names.
        """
        final_upload_path = "{upload_start_path}{filename_final}".format(
                                 upload_start_path=upload_start_path,
                                 filename_final=filename_final,
                            )
        if filename_req and file_extension:
            """
            Save the eventual path to the Django-steItem instance
            """
            file_obj.path = final_upload_path
            file_obj.save()

        policy_document_context = {
            "expire": policy_expires,
            "bucket_name": settings.S3_CONFIG.get('AWS_UPLOAD_BUCKET'),
            "key_name": "",
            "acl_name": "private",
            "content_name": "",
            "content_length": 524288000,
            "upload_start_path": upload_start_path,

            }
        policy_document = """
        {"conditions": [ 
            {"bucket": "%(bucket_name)s"}, 
            ["starts-with", "$key", "%(upload_start_path)s"],
            {"acl": "%(acl_name)s"},
            
            ["starts-with", "$Content-Type", "%(content_name)s"],
            ["starts-with", "$filename", ""],
            ["content-length-range", 0, %(content_length)d]
          ]
        }
        """ % policy_document_context

        aws_secret = str.encode(settings.S3_CONFIG.get('AWS_UPLOAD_SECRET_KEY'))
        policy_document_str_encoded = str.encode(policy_document.replace(" ", ""))
        bucket=settings.S3_CONFIG.get('AWS_UPLOAD_BUCKET')
        minioClient = MC.getInstance()
        url = minioClient.client.presigned_put_object(bucket, final_upload_path)
        policy = base64.b64encode(policy_document_str_encoded)
        signature = base64.b64encode(hmac.new(aws_secret, policy, hashlib.sha1).digest())
        data = {
            # "policy": policy,
            # "signature": signature,
            "key": settings.S3_CONFIG.get('AWS_UPLOAD_ACCESS_KEY_ID'),
            "file_bucket_path": upload_start_path,
            "file_id": file_obj_id,
            "filename": filename_final,
            "url": url,
            "token": token,
        }
        return Response(data, status=status.HTTP_200_OK)
