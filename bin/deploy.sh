#!/bin/bash
##################################################
##################################################
# Deployment for cloud function -     Covid19Bot #
##################################################
##################################################

# Setting some parameters for the deployer. This will likely be done by Jenkins or something.
PROJECT=impostobot

pipenv lock -r > ./covidbot/requirements.txt
cd covidbot # Move to the folder with the scripts and necessary files

# Now we do the actual deploy.
gcloud functions deploy covid19bot \
    --region us-east4 \
    --env-vars-file=keys.yaml \
    --runtime python37 \
    --trigger-http \
    --entry-point main \
    --memory 256MB \
    --project $PROJECT 

cd ..