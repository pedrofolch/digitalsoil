import datetime


AWS_ACCESS_KEY_ID = "AKIAJJOCCBOZY4DKFMGA"
AWS_SECRET_ACCESS_KEY = "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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

AWS_UPLOAD_BUCKET = 'projectdigitalsoil'

AWS_UPLOAD_USERNAME = 'pedrofolch'

AWS_UPLOAD_GROUP = 'digital_soil_group'

AWS_UPLOAD_REGION = 'us-west-1'

AWS_UPLOAD_ACCESS_KEY_ID = "AKIAIM5CIECJSYJ5E4HQ"

AWS_UPLOAD_SECRET_KEY = "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"

DEFAULT_FILE_STORAGE = 'digitalSoil.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'digitalSoil.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'projectdigitalsoil'
S3DIRECT_REGION = 'us-west-1'
AWS_DEFAULT_ACL = None
AWS_S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL

STATIC_URL = AWS_S3_URL + '/static/'
STATICFILES_LOCATION = 'media'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': 'thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}
