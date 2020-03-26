#!/bin/bash
##################################################
##################################################
# Deployment for cloud function -     Covid19Bot #
##################################################
##################################################

PROJECT=impostobot

pipenv lock -r > ./covidbot/requirements.txt
cd covidbot # Move to the folder with the scripts and necessary files

# Now we do the actual deploy.
gcloud functions deploy covid19bot \
    --region us-central1 \
    --env-vars-file=keys.yaml \
    --runtime python37 \
    --trigger-http \
    --entry-point main \
    --memory 256MB \
    --project $PROJECT 

cd ..