MYSQL = {
    'host': 'mysql',
    #'host': '127.0.0.1',
    'port': 3306,
    'db': 'hasty_database',
    'username': 'root',
    'password': '',
    'test_db': 'test_hasty_database'
}

RABBIT_MQ = {
    'host': 'rabbitmq',
    # 'host': '127.0.0.1:5672',
    'user': 'admin',
    'password': 'mypass',
    'vhost': ''
}

# S3_CONFIG = {
#     "MINIO_ENDPOINT": '127.0.0.1:9001',
#     # "MINIO_ENDPOINT": "public.examplemin.io:9001",
#     "AWS_UPLOAD_BUCKET" : "hasty-media",
#     "AWS_UPLOAD_REGION" : "us-east-2",
#     "AWS_UPLOAD_ACCESS_KEY_ID" : "minio",
#     "AWS_UPLOAD_SECRET_KEY" : "minio123"
#     "SECURE": False
# }
S3_CONFIG = {
    "MINIO_ENDPOINT": 'play.min.io',
    "AWS_UPLOAD_BUCKET" : "hasty-media",
    "AWS_UPLOAD_REGION" : "",
    "AWS_UPLOAD_ACCESS_KEY_ID" : "Q3AM3UQ867SPQQA43P2F",
    "AWS_UPLOAD_SECRET_KEY" : "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
    "SECURE": True
}


