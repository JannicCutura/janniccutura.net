import boto3
import os
from tqdm import tqdm
import shutil
import subprocess

# define resrouces
s3 = boto3.resource('s3')
BUCKET = "janniccutura.net"



# delete all files
os.listdir('public')
shutil.rmtree('public', ignore_errors=False, onerror=None)

subprocess.Popen("del /S *", cwd='C:/Users/janni/Dropbox/website/janniccutura.net/public')


# genereate production files
subprocess.Popen("hugo -D", cwd='C:/Users/janni/Dropbox/website/janniccutura.net')


# upload to s3
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
