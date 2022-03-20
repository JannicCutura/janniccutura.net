# build the website

1. open poewrshell admin in this folder `hugo2\startrt-academic`
2. `hugo server` to view locally
3. Delete all files from `public`
4. `hugo -D` to generate files to `public`

then

5. still in same cmd run: `aws s3 sync public/ s3://janniccutura.net/ --delete --acl public-read`

or
 
5. copy everything from public to S3. (automate this). Careful to not forget folders, drag and drop!!

finally to incalited cloudfront immediately:

6. Cmd `aws cloudfront create-invalidation --distribution-id  EWSY4HMP2EXL0  --paths "/*"` to force an update. careful only certain free amounts. 




