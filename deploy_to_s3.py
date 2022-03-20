import boto3
import os
from tqdm import tqdm
import shutil
import subprocess
import time
# define resrouces
s3 = boto3.resource('s3')
BUCKET = "janniccutura.net"



# delete all files
try:
    shutil.rmtree('public', ignore_errors=False, onerror=None)
    subprocess.Popen("del /S *", cwd='C:/Users/janni/Dropbox/website/janniccutura.net/public')
except:
    print("Folder empty already")


# genereate production files
subprocess.Popen("hugo -D", cwd='C:/Users/janni/Dropbox/website/janniccutura.net')
time.sleep(30)

# delete all files
my_bucket = s3.Bucket(BUCKET)
for my_bucket_object in tqdm(my_bucket.objects.all()):
    s3.Object(BUCKET, my_bucket_object.key).delete()



# upload to s3
website_files = []
for path, currentDirectory, files in os.walk(os.getcwd()+'\public'):
    for file in files:
      website_files.append(os.path.join(path, file))

website_files = [website_file[55:].replace('\\','/') for website_file in website_files ]
website_files

for file in tqdm(website_files):
  s3.Bucket(BUCKET).upload_file("public/"+file, file)



import boto3
import mimetypes

bucket = s3.Bucket("janniccutura.net")

local_root=r'C:/Users/janni/Dropbox/website/janniccutura.net'
local_dir="/public"

for root, dirs, files in os.walk(local_root + local_dir):
    for filename in files:
        # construct the full local path (Not sure why you were converting to a
        # unix path when you'd want this correctly as a windows path
        local_path = os.path.join(root, filename)
        print(local_path)
        # construct the full S3 path
        relative_path = os.path.relpath(local_path, local_root)

        s3_path = relative_path.replace(os.path.sep,"/")
        print(relative_path)
        print(s3_path)

        # Get content type guess
        content_type = mimetypes.guess_type(filename)[0]
        bucket.upload_file(
            local_path,
            s3_path,
            ExtraArgs={'ACL': 'public-read', 'ContentType': content_type}
        )


# INvalidate old files on cloudfront
if False:
    subprocess.Popen('aws cloudfront create-invalidation --distribution-id  EWSY4HMP2EXL0  --paths "/*"')
