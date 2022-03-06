import boto3
import os
from tqdm import tqdm

s3 = boto3.resource('s3')
BUCKET = "janniccutura.net"

os.listdir()

import os
website_files = []
for path, currentDirectory, files in os.walk(os.getcwd()+'\public'):
    for file in files:
      website_files.append(os.path.join(path, file))

website_files = [website_file[55:].replace('\\','/') for website_file in website_files ]
website_files

for file in tqdm(website_files):
  s3.Bucket(BUCKET).upload_file("public/"+file, file)



#s3.Bucket(BUCKET).upload_file("public/talk/example-talk/featured.jpg", "talk/example-talk/featured.jpg")
