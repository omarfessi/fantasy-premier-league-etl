---

# Fantasy Premier League ETL

![Python](https://img.shields.io/badge/Python-61.9%25-blue)
![HCL](https://img.shields.io/badge/HCL-32.3%25-green)
![Shell](https://img.shields.io/badge/Shell-4%25-lightgrey)
![Dockerfile](https://img.shields.io/badge/Dockerfile-1.8%25-blue)

## Overview
This project is an Extract, Load, Transform (although a set of transformation/validation is applied before loading data) pipeline designed to fetch and process data from the Fantasy Premier League (FPL) API. 
The data will some day serve data visualisation tool.

## Features
- **Data Extraction**: Fetches data from the FPL API.
- **Data Transformation**: Cleans and processes raw data into a structured format using DBT.
- **Data Loading**: Loads transformed data into a data warehouse for analysis.
- **Dockerized**: Runs the ETL pipeline in a Docker container for easy deployment.
- **Infrastructure as Code**: Managed using HCL Terraform for reproducible infrastructure.

## Getting Started

### Prerequisites
- Docker
- Python 3
- Terraform
- DBT
- Google Cloud Account

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/omarfessi/fantasy-premier-league-etl.git
    cd fantasy-premier-league-etl
    ```

2. Set up the Python environment:
    ```sh
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### Running the ELT Pipeline
* The Extract process is intended to run in a Cloud Run environment which is triggered by a Cloud Scheduler job that runs every day at 10 PM UTC, for development purpose or testing, you could as well use the bash script ```
./run.sh (which as for today not complete, but is functional) 
* The Load process intends to push parquet files to GCS from the previous step, in this step a cloud function loads these parquets to Bigquery table.
* The Transform process uses DBT on Bigquery, which runs in a Cloud Run environment. 

## Repository Structure

```plaintext
.
├── cloud_run_ingestion
│   ├── Dockerfile
│   ├── ingestion
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── pipeline.py
│   │   └── utilities.py
│   └── requirements.txt
├── cloud_run_modeling
│   ├── Dockerfile
│   └── modeling
│       ├── dbt_project.yml
│       ├── models
│       │   ├── dimensions
│       │   │   ├── players_cleansed.sql
│       │   │   └── teams_cleansed.sql
│       │   ├── facts
│       │   │   ├── events_cleansed.sql
│       │   │   ├── flat_fixtures.sql
│       │   │   └── unit_test_flat_fixtures.yml
│       │   ├── marts
│       │   │   └── goals_contributions.sql
│       │   └── properties.yml
│       ├── package-lock.yml
│       ├── packages.yml
│       ├── profiles.yml
│       ├── seeds
│       │   ├── properties.yml
│       │   └── stat_points.csv
│       ├── snapshots
│       └── tests
├── cloudbuild.yaml
├── load_parquet_to_bq_cf
│   ├── main.py
│   └── requirements.txt
├── pyproject.toml
├── run.sh
├── scripts
│   ├── cloud_build.sh
│   ├── run.sh
│   └── update_job.sh
├── terraform
│   ├── backend.tf
│   ├── locals.tf
│   ├── main.tf
│   ├── modules
│   │   ├── gcf_creation
│   │   │   ├── main.tf
│   │   │   └── variables.tf
│   │   └── gcf_sa_permissions
│   │       ├── main.tf
│   │       ├── output.tf
│   │       └── variables.tf
│   ├── provider.tf
│   └── variables.tf
└── tests
    ├── conftest.py
    ├── test_pipeline.py
    └── test_utilities.py
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact
For any inquiries, please contact Omar Fessi at omarfessy@gmail.com.

---
