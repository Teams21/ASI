#!/usr/bin/zsh

# Run only on WSL2 with Docker installed and started (sudo service docker start)
docker run  -it --rm -v ~/.aws:/root/.aws -v ${PWD}/data/05_models/model:/app/data/05_models/model/ -e WANDB_API_KEY='8cc7cb0fc715e9dbe616278bdd599025d526f34c' -e POSTGRES_CONNECTION_STRING='postgresql://postgres:3aFwVWE5B2vwSYDObcGY@asi-postgres.cxakwoumaypu.eu-central-1.rds.amazonaws.com:5432/ASI' -e PSYCOPG_CONNECTION_STRING='ASI:postgres:3aFwVWE5B2vwSYDObcGY:asi-postgres.cxakwoumaypu.eu-central-1.rds.amazonaws.com:5432' asi:1.0 /bin/bash
