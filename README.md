# ASI

The project is an MLOps pipeline that aims to:
 - train a model to classify a person as depressed or not depending on the eye movements, tracked by BeGaze2
 - deploy the model and make it accessible for anyone in the internet

Prerequisites:
 - python 3.11 installed
 - miniconda installed

Steps to run:
 1. clone the repo
 2. cd ASI
 3. create the virtual environment by running 'conda env create -f environment.yml'
 4. if the environment is not activated, run 'conda activate kedro-environment'
 4. install extra dependencies with 'pip install -r requirements.txt'
 5. run 'kedro run'
