# ASI

The project is an MLOps pipeline that aims to:
 - train a model to classify a person as depressed or not depending on the eye movements, tracked by BeGaze2
 - deploy the model and make it accessible for anyone in the internet

## Table of Contents
1. [Introduction](#introduction)
2. [Context](#context)
3. [Detailed Column Descriptions](#detailed-column-descriptions)
4. [Wizualizacja pipeline'ów]()
5. [Prerequisites](prerequisites)
6. [Requirements](#requirements)
7. [Setup Environment](#setup-environment)
8. [Running the Application](#running-the-application)
9. [Setup Development](#setup-development)

## Introduction
In this application, we utilize eye movement data tracked by BeGaze2 to train a model that classifies individuals as depressed or not. Our goal is to create a tool capable of providing rapid and accurate depression assessments based on the analysis of eye movement patterns, aiming to enhance mental health diagnostics.
## Context
Research on eye movements in the context of mental health focuses on analyzing how these patterns can reflect an individual's emotional and psychological state. By tracking eye movements, scientists aim to identify biomarkers associated with depression, anxiety, and other mental disorders. Technologies like BeGaze2 enable precise and non-invasive studies that support early detection, diagnosis, and monitoring of psychological therapies' effects.
## Detailed Column Descriptions
* Stimulus - Stimulus name.
* Export Start Trial Time [ms] - Export start time, normally zero.
* Export End Trial Time [ms] -  Export end time.
* Participant - Participant name.
* Color: The color of the stimulus element that was presented.
* Eye L/R - Which eye fixated inside an AOI.
* AOI Name - Area of interest name
* AOI Group - AOI Group name
* AOI Scope -  AOI Scope(global: AOI present in all stimuli, local: AOI present in one stimulus only)
* AOI Order - AOI depth order on the Z axis
* AOI Size [px] - Size of AOI in pixel - the part overlapping the stimulus is taken into consideration, parts outside 
the stimulus area are ignored. For dynamic AOIs the size is the sum of sizes at each sample timestamp (as defined above) where the AOI is visible averaged by the number of samples where the AOI is visible.
* AOI Coverage [%] - AOI size in comparison to Stimulus size.
* Time to First Appearance [ms] -  Time when the AOI becomes visible for the first time relative to the trial start.
* Appearance Count - Sum of all appearances of one AOI  within the stimulus (the number of sliceswhere the AOI was visible).
* Visible Time [ms] - Sum of AOI duration within one trial– For static AOI it is end time – start time– For dynamic AOI it is the sum of all durations where the AOI was visible within start and end time.
* Visible Time [%] - Visible time (ms) / (end time - start time).
* Entry Time [ms] -  Duration from start of the trial to the first fixation hit of the AOI (fixation position is inside the AOI).
* Sequence - Order of gaze hits into the AOIs based on Entry Time, lowest Entry Time = first in sequence.
* Net Dwell Time [ms] - Sum of sample durations for all gaze data samples that hit the AOI. 
* Dwell Time [ms] - Dwell Time is the sum of all Dwell Times for each visit of an AOI. Dwell Time for one visit is the sum of durations of all saccades and fixations inside the AOI.
* Normalized Dwell [ms/Coverage] - Dwell time divided by AOI Coverage.
* Glance Duration [ms] - Saccade duration for entering the object + sum of all fixation durations and saccade durations before the eyes begin to leave the AOI = dwell time + duration of saccade entering AOI. (*)
* Diversion Duration [ms] - Duration of the first fixation to hit the AOI.
* First Fixation Duration [ms] -  The duration of the first fixation in an AOI(if any).
* Glances Count - Number of glances to a target (saccades coming from outside) within a certain period (increment the   each time a fixation hits the AOI, if not hit before).[both eyes].
* Revisits - Glances count - 1.
* Fixation Count - Number of fixations inside the AOI.
* Net Dwell Time [%] - Net dwell time (ms) / (end time - start time).
* Dwell Time [%] - Dwell time (ms) / (end time - start time).
* Fixation Time [ms] - Sum of the fixation durations inside the AOI.
* Fixation Time [%] - Fixation time (ms) / (end time - start time).
* Average Fixation Duration [ms] - The sum of fixation times divided by number of fixations inside an AOI.
## Wizualizacja pipeline'ów
![image](https://github.com/Teams21/ASI/assets/21336128/773407a6-0dc9-4d2c-9aaf-17b072836605)
## Prerequisites 
- miniconda installed
## Requirements
- anyio==3.7.1
- binaryornot==0.4.4
- category-encoders==2.6.3
- click-default-group==1.2.4
- conda==22.9.0
- Cython==3.0.10
- docker-pycreds==0.4.0
- fastapi==0.110.1
- graphql-core==3.2.3
- hpack==4.0.0
- httptools==0.6.1
- imbalanced-learn==0.12.2
- joblib==1.3.2
- kedro-telemetry==0.3.2
- kedro-viz==9.0.0
- llvmlite==0.42.0
- matplotlib==3.7.5
- munkres==1.1.4
- packaging==23.2
- pandas==1.5.3
- pathtools==0.1.2
- pmdarima==2.0.4
- protobuf==4.25.3
- pyarrow==15.0.2
- pycaret==3.3.1
- pydantic_core==2.18.1
- pyod==1.1.3
- python-dotenv==1.0.1
- python-editor==1.0.4
- pywin32==306
- retrying==1.3.3
- ruff==0.1.15
- scikit-base==0.7.7
- scikit-plot==0.3.7
- scipy==1.11.4
- secure==0.3.0
- sktime==0.26.0
- strawberry-graphql==0.226.0
- tbats==1.1.3
- threadpoolctl==3.4.0
- torch==2.0.1
- watchfiles==0.21.0
- watchgod==0.8.2
- yellowbrick==1.5
- zstandard==0.22.0
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
