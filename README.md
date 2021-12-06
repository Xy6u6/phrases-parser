# phrases-parser
Program, that parsing site of phrases, collect it into /tmp/scrapper/ files by it's tag name
uploads saved files into GCS bucket and than, transfers data from GCS bucket files to bigquery table
requirements to start: 
      
 docker, docker-compose

Steps to start:

  - clone github repo
   
        $git clone git@github.com:Xy6u6/phrases-parser.git
  
  
  - add private key file of google storage acc(this file was given to you when you created the service account
   this file must contain a JSON object with a private key and other credentials information (downloaded from the Google APIs console)) to project directory
   and replace YOUR_PRIVATE_KEY_FILE.json in Dockerfile to your private key file name
  
  
        COPY ./YOUR_PRIVATE_KEY_FILE.json ./tmp/gcp-acc.json


  - from your cloned directory run in terminal
        
        $docker-compose up --build
