# ASI

The project is an MLOps pipeline that aims to:
 - train a model to classify a person as depressed or not depending on the eye movements, tracked by BeGaze2
 - deploy the model and make it accessible for anyone in the internet

## Table of Contents
1. [Introduction](#introduction)
2. [Context](#context)
3. [Content](#content)
4. [Detailed Column Descriptions](#detailed-column-descriptions)
5. [Training Method](#training-method)
6. [Prerequisites](prerequisites)
7. [Requirements](#requirements)
8. [Setup Environment](#setup-environment)
9. [Running the Application](#running-the-application)
10. [Setup Development](#setup-development)

## Introduction
In this application, we utilize eye movement data tracked by BeGaze2 to train a model that classifies individuals as depressed or not. Our goal is to create a tool capable of providing rapid and accurate depression assessments based on the analysis of eye movement patterns, aiming to enhance mental health diagnostics.
## Context
Research on eye movements in the context of mental health focuses on analyzing how these patterns can reflect an individual's emotional and psychological state. By tracking eye movements, scientists aim to identify biomarkers associated with depression, anxiety, and other mental disorders. Technologies like BeGaze2 enable precise and non-invasive studies that support early detection, diagnosis, and monitoring of psychological therapies' effects.
## Content
## Detailed Column Descriptions
## Training Method
## Prerequisites 
- miniconda installed
## Requirements
anyio==3.7.1
binaryornot==0.4.4
category-encoders==2.6.3
click-default-group==1.2.4
conda==22.9.0
Cython==3.0.10
docker-pycreds==0.4.0
fastapi==0.110.1
graphql-core==3.2.3
hpack==4.0.0
httptools==0.6.1
imbalanced-learn==0.12.2
joblib==1.3.2
kedro-telemetry==0.3.2
kedro-viz==9.0.0
llvmlite==0.42.0
matplotlib==3.7.5
munkres==1.1.4
packaging==23.2
pandas==1.5.3
pathtools==0.1.2
pmdarima==2.0.4
protobuf==4.25.3
pyarrow==15.0.2
pycaret==3.3.1
pydantic_core==2.18.1
pyod==1.1.3
python-dotenv==1.0.1
python-editor==1.0.4
pywin32==306
retrying==1.3.3
ruff==0.1.15
scikit-base==0.7.7
scikit-plot==0.3.7
scipy==1.11.4
secure==0.3.0
sktime==0.26.0
strawberry-graphql==0.226.0
tbats==1.1.3
threadpoolctl==3.4.0
torch==2.0.1
watchfiles==0.21.0
watchgod==0.8.2
yellowbrick==1.5
zstandard==0.22.0
## Setup Environment
Steps to run from Anaconda Prompt (miniconda 3):
 1.  clone the repo 'git clone git@github.com:Teams21/ASI.git'
 2.  cd ASI
 3.  create the virtual environment by running 'conda env create -f environment.yml'
 4.  if the environment is not activated, run 'conda activate kedro-environment'
 5.  install extra dependencies with 'pip install -r requirements.txt'
 6.  install postgres connection string file by running 'copy z:\credentials.yml conf/local/'
 7.  install aws cli
 8.  add aws user by running 'aws configure --profile asi-s3-reader'
 9.  run 'kedro run'
 10. optionally run 'kedro viz' for visualisation

## Running the Application

 In case there is a problem with environment setup: (not fully tested)
  1. create a new conda environment called kedro-environment
  2. activate the environment
  3. install mamba
  4. run 'mamba env update --file environment.yml --name kedro-environment'
