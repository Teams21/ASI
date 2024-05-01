# ASI

The project is an MLOps pipeline that aims to:
 - train a model to classify a person as depressed or not depending on the eye movements, tracked by BeGaze2
 - deploy the model and make it accessible for anyone in the internet

Prerequisites:
 - miniconda installed

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

 In case there is a problem with environment setup: (not fully tested)
  1. create a new conda environment called kedro-environment
  2. activate the environment
  3. install mamba
  4. run 'mamba env update --file environment.yml --name kedro-environment'