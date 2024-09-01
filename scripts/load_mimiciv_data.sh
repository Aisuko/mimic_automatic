#!/bin/bash

source .env


psql -h ${POSTGRES_ADDRESS} -p ${POSTGRES_PORT} -U ${POSTGRES_USERNAME} -d ${POSTGRES_DB} -c "\l"


psql -h ${POSTGRES_ADDRESS} -p ${POSTGRES_PORT} -U ${POSTGRES_USERNAME} -d ${POSTGRES_DB} -f mimic-iv/buildmimic/postgres/create.sql

# Load data into PostgreSQL
psql -h ${POSTGRES_ADDRESS} -p ${POSTGRES_PORT} -U ${POSTGRES_USERNAME} -d ${POSTGRES_DB} -v ON_ERROR_STOP=1 -v mimic_data_dir=${MIMIC_DATA_DIR} -f mimic-iv/buildmimic/postgres/load_gz.sql

# # Apply constraints
psql -h ${POSTGRES_ADDRESS} -p ${POSTGRES_PORT} -U ${POSTGRES_USERNAME} -d ${POSTGRES_DB} -v ON_ERROR_STOP=1 -v mimic_data_dir=${MIMIC_DATA_DIR} -f mimic-iv/buildmimic/postgres/constraint.sql

# # Create indexes
psql -h ${POSTGRES_ADDRESS} -p ${POSTGRES_PORT} -U ${POSTGRES_USERNAME} -d ${POSTGRES_DB} -v ON_ERROR_STOP=1 -v mimic_data_dir=${MIMIC_DATA_DIR} -f mimic-iv/buildmimic/postgres/index.sql


