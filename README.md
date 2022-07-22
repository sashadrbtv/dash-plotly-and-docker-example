# Dash App (Plotly) & Docker implementation

### Task
In this exercise, you are given a dataset with claims data. 
Business users are interested to see trends and 
anomalies in the data as well as projections for the upcoming 6 months.

Note: Claims are expenses that insurance companies have to pay for medical services provided to patients.

### Dataset
This dataset is a sampled aggregated data for the period of 2018/01 - 2020/07 (numbers are fictional). 

The dataset contains the following columns:

    MONTH - a month claims were lodged
    SERVICE_CATEGORY - a department that provided services to patients
    CLAIM_SPECIALTY - a type of medical services by an official classification system
    PAYER - an insurance company
    PAID_AMOUNT - sum of expenses (claims), $


### Docker setup

create image: `docker build -t dash .` <br />
run container with the application: `docker compose up` <br />
go to `http://127.0.0.1:8050/` in browser


### Manual setup

build environment: `python3.8 -m venv env` <br />
upload packages: `env/bin/pip install -r requirements.txt`


