# HastyImages

## Steps to setup the project using Docker

NOTE: you will require git and docker installed on your machine

*Step 1:* Git clone the repository and go to project folder
```
    $ git clone git@github.com:shezadaibara/HastyImages.git
    $ cd HastyImages
```
_Note:_ `docker-compose.yml` file is in `HastryImages` folder

*Step 2:* Build the docker container using docker-compose
```
    $ docker-compose build
```

*Step 3:* Start the docker container using docker-compose
```
    $ docker-compose up 
    (optional: use `-d` argument to run as a deamon)
```

The Project is up and running at this point.

To delete and restart the docker containers do
```
    $ docker-compose down 
    (optional: use `-v` argument to delete all the volumes (i.e: databases))
    $ docker-compose up
```

## Architecture Explanation:
This project assumes that an invitation is sent to a person. which provides an upload_link to the end-user. using this upload link the user will be able to upload 1 or many images using his browser. 

Uploading Images functionality is client heavy, which means all the heavy work of uploading the image to object storage service and reading metadata of the image file is done at the client (in our case web browser). In the mean time the 

*Key Decision:* Object Storage service used by this project is called `MinIO`. It is very similar to Aws S3 but free to use. Ideally one need to build their own MinIO Server. but for the purpose of this example I am the free to use test server http://paly.min.io to upload images.

An access_token is used to give access to the end-user, all access_tokens have a default expiry time of 7 days, an invalid/expired token throw a 403-forbidden response.


### Uploading Images functionality explained in details:

-> To get the upload link use the POST `api/invitations` API endpoint. use a latest browser to open upload_link
-> The upload_link provided to the end-user renders a django template called `upload.html`
-> upload.html contains a file form to upload files (use `Shift` to select multiple) directly to the minio server
-> forEach file selected by the user
    a> Makes call to HastyImage server :  POST `api/files/policy` : 
        - this endpoint is used to create an image object in the db
        - store some basic data like (size, file_type, etc) in the image object
        - gets a `presigned_put_object URL` called `upload_link`: a minIO server url which is valid for only 1day and used to upload the image to storage   
    b> upload File to storage is done use an XHR request. take small chunks of the image file and uploads it to the storage. eventListers are used on this xhr request
    c> on load event: the progress bar is updates
    d> on complete event:  
        > fetch the metadata of the image:
        > notifies the HastyImage server using POST Api `api/files/complete` that image has completed uploading and also store the images metadata
    
-> Finally  Get `api/images` end point can be used to list all the images for a given token. the api also provides presigned_get_object URL called `image_link`: a minIO server url which is valid for only 1day and used to get the image from storage


## Api Desc:
    
1. getInvitation (uploadLink) Api

An Api endpoint to get the invite to upload_link
URL:
```POST : localhost:8000/invitation/```

Payload
```
{
    email : <email_address>
}
```
Response
```
{
    "token": "41913f22-7fb1-4b6b-9396-5d68873b960c",
    "email": "<emaill_address>",
    "created_at": "<datetime>",
    "updated_at": "2019-08-27T07:40:44.851229Z",
    "expires_at": "2019-09-03T07:40:44.834132Z",
    "upload_link": "http://localhost:8000/api/upload/?access_token=41913f22-7fb1-4b6b-9396-5d68873b960c"
}
```
Note: Multiple Request with the same payload will extend a token expiration to 7days starting now()


2. GetListImages Api
Get the list of All the images for a given token. 
URL 
```GET localhost:8000/api/images/?access_token=a7822df7-7fb7-4f8b-a7d6-4115d8e5af0b```

query_params
```
{ "access_token" : <uuid> }
```
Response
```
[	{
        "name": "Nikon_COOLPIX_P1.jpg",
        "path": "<token>/<id>/<id>.jpg", # path in the storage
        "size": <file-size>,
        "file_type": "<image-file-type>",
        "timestamp": "2019-08-27T06:01:52.178644Z",
        "updated": "2019-08-27T06:01:52.927848Z",
        "uploaded": true,
        "active": true,
        "token": "<UUID>",
        "make": "NIKON",
        "model": "COOLPIX P1",
        "xDimension": 100,
        "yDimension": 75,
        "orientation": 1,
        "software": "GIMP 2.4.5",
        "flash": "Flash did not fire, auto mode",
        "metering_mode": "Pattern",
        "saturation": "Normal",
        "sharpness": "Normal",
        "contrast": "Normal",
        "x_resolution": "72",
        "y_resolution": "72",
        "aperture_value": "2.9",
        "focal_length": "7.5",
        "exif_version": "0220",
        "image_link": "<http image_link url>" # read image_link of the token with 
    },
]	
```

3. CreateImageItem Api
An Api endpoint to create the image object in data and return the image's upload_link that can be 
used by the client to store image in minIO storage 

URL:
```
    POST : api/files/policy?access_token={access_token}
```

QueryParams
```
    { "access_token" : <uuid> }
```
Payload
```
{"filename":"<filename.extension>"}
```
Response
```
{
    "key": "<storage_access_key>",
    "file_bucket_path": "<path/to/the/file>",
    "file_id": <id>,
    "filename": "<file.ext>",
    "url": "<upload-link url>", # PUT url to upload image to minIO
    "token": "<uuid>"
}
```

4. ImageUploadCompleate Api
URL:
```
    POST : api/files/policy?access_token={access_token}
```
QueryParams
```
    { "access_token" : <uuid> }
```
Payload
```
{
	"uploaded": true,
	"fileSize": 4278,
	"file": 11,
	"fileType": "image/jpeg",
	"metadata": "{}"
}
```
Response
```
{}
```