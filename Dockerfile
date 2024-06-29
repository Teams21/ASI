FROM python:3.10

WORKDIR /app
RUN apt-get -y update && apt-get install -y \
    python3-dev \
    apt-utils \
    build-essential \
    && rm -rf /var/lib.apt/lists*

RUN pip3 install -U setuptools
RUN pip3 install \
    cython==3.0.6 \
    numpy==1.26.0 \
    pandas==2.1.4 \
    kedro[all] \
    kedro-viz \
    wandb==0.16.5 \
    boto3==1.34.69 \
    sqlalchemy==2.0.29 \
    psycopg2==2.9.9 \
    scikit-learn==1.4.2 \
    setuptools==69.5.1 \
    wheel==0.43.0

RUN pip3 install torch==2.3.1 torchvision==0.18.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install autogluon

COPY conf/ /app/conf/
COPY src/ /app/src/
COPY pyproject.toml /app/
CMD kedro run
