# Kidney Disease Classification — MLOps

An end-to-end deep learning pipeline that classifies kidney CT scan images (**Normal / Cyst / Tumor / Stone**) using transfer learning (VGG16), wired up with a full MLOps stack: modular pipeline code, experiment tracking with **MLflow**, data & pipeline versioning with **DVC**, a **Flask** web app for inference, and **CI/CD deployment to AWS** via GitHub Actions and Docker.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Pipeline Stages](#pipeline-stages)
- [Getting Started](#getting-started)
- [Running the DVC Pipeline](#running-the-dvc-pipeline)
- [Experiment Tracking with MLflow / DagsHub](#experiment-tracking-with-mlflow--dagshub)
- [Running the App](#running-the-app)
- [CI/CD Deployment (AWS + GitHub Actions)](#cicd-deployment-aws--github-actions)
- [Development Workflow](#development-workflow)

---

## Overview

This project trains a CNN-based image classifier (VGG16 backbone, fine-tuned) to detect kidney conditions from CT scan images. Beyond the model itself, the repo demonstrates a production-style ML workflow:

- Modular, reusable pipeline code organized as an installable Python package (`cnnclassifier`)
- Configuration-driven design (`config.yaml`, `params.yaml`) instead of hardcoded values
- Reproducible pipelines via **DVC**, so stages only re-run when their inputs actually change
- Experiment tracking and model logging via **MLflow**, backed by **DagsHub**
- A lightweight **Flask** app for serving predictions
- Containerized deployment to **AWS (EC2 + ECR)** through a self-hosted GitHub Actions runner

## Tech Stack

| Layer | Tools |
|---|---|
| Modeling | TensorFlow / Keras (VGG16 transfer learning) |
| Pipeline orchestration | DVC |
| Experiment tracking | MLflow, DagsHub |
| Serving | Flask |
| Packaging | `setup.py`, local package `src/cnnclassifier` |
| CI/CD | GitHub Actions, Docker, AWS ECR + EC2 |

## Project Structure

```
├── .github/workflows/      # CI/CD pipeline (build → push to ECR → deploy on EC2)
├── config/
│   └── config.yaml         # Paths & static configuration for each pipeline stage
├── research/                # Jupyter notebooks used to prototype each pipeline stage
├── src/cnnclassifier/       # Core installable package
│   ├── components/          # Data ingestion, base model prep, training, evaluation
│   ├── config/               # ConfigurationManager — reads config/params into entities
│   ├── entity/                # Config dataclasses for each stage
│   ├── pipeline/              # Orchestrates components into runnable stages
│   └── utils/                 # Common helpers (YAML/JSON I/O, directory creation, etc.)
├── templates/                # HTML templates for the Flask app
├── dvc.yaml                  # DVC pipeline definition (stages, deps, outputs)
├── params.yaml                # Model/training hyperparameters
├── main.py                    # Entry point that runs the full pipeline stage-by-stage
├── app.py                     # Flask app for serving predictions (training + inference routes)
├── setup.py                   # Makes `cnnclassifier` pip-installable
├── template.py                 # Script that scaffolds the project's folder/file structure
└── requirements.txt
```

## Pipeline Stages

The pipeline is broken into independent, DVC-tracked stages, each with its own config, component, and entry point:

1. **Data Ingestion** — downloads and unzips the kidney CT scan dataset
2. **Prepare Base Model** — loads VGG16 pretrained on ImageNet, adds a custom classification head, freezes/unfreezes layers as configured
3. **Model Training** — fine-tunes the model on the kidney dataset using parameters from `params.yaml`
4. **Model Evaluation** — evaluates the trained model and logs metrics/artifacts to MLflow

Each stage reads its settings through the `ConfigurationManager`, which merges `config/config.yaml` and `params.yaml` into typed config entities — so changing a hyperparameter or path never requires touching pipeline code.

## Getting Started

### Prerequisites
- Python 3.8+
- Conda (recommended) or `venv`
- Git

### 1. Clone the repository

```bash
git clone https://github.com/amitkumar8178/Kidney-Disease-Classification-MLOps.git
cd Kidney-Disease-Classification-MLOps
```

### 2. Create and activate an environment

```bash
conda create -n cnncls python=3.8 -y
conda activate cnncls
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the DVC Pipeline

Instead of running scripts manually, the whole pipeline can be driven by DVC so that only the affected stages re-run when inputs change:

```bash
dvc init
dvc repro
dvc dag
```

Alternatively, run the full pipeline directly:

```bash
python main.py
```

## Experiment Tracking with MLflow / DagsHub

Experiments (parameters, metrics, and model artifacts) are logged to MLflow, backed by a DagsHub remote tracking server.

Set the following environment variables before running training/evaluation (get the values from your own DagsHub repo settings):

```bash
export MLFLOW_TRACKING_URI=<your-dagshub-mlflow-uri>
export MLFLOW_TRACKING_USERNAME=<your-dagshub-username>
export MLFLOW_TRACKING_PASSWORD=<your-dagshub-token>
```

To view experiments locally instead:

```bash
mlflow ui
```

> **Note:** Never commit MLflow/DagsHub credentials to the repo — store them as environment variables or GitHub Actions secrets.

**MLflow vs DVC, in short:**

| | MLflow | DVC |
|---|---|---|
| Purpose | Experiment tracking, model logging, tagging | Lightweight pipeline orchestration & data/artifact versioning |
| Best for | Comparing runs, production-grade experiment history | Fast POC pipelines with reproducible stages |

## Running the App

```bash
python app.py
```

Then open the printed local host and port in your browser to use the web interface for predictions.

## CI/CD Deployment (AWS + GitHub Actions)

The included GitHub Actions workflow builds a Docker image, pushes it to Amazon ECR, and deploys it on an EC2 instance configured as a self-hosted runner.

**High-level flow:**
1. Build the Docker image from source
2. Push the image to ECR
3. Pull the image on the EC2 instance
4. Run the container on EC2

### Setup steps

1. **Create an IAM user** with the following policies:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonEC2FullAccess`
2. **Create an ECR repository** to store the Docker image, and note its URI.
3. **Launch an EC2 instance** (Ubuntu).
4. **Install Docker on EC2:**
   ```bash
   sudo apt-get update -y
   sudo apt-get upgrade -y

   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```
5. **Register the EC2 instance as a self-hosted GitHub Actions runner**
   (Settings → Actions → Runners → New self-hosted runner → follow the OS-specific commands).
6. **Add the following GitHub repository secrets:**

   | Secret | Description |
   |---|---|
   | `AWS_ACCESS_KEY_ID` | IAM user access key |
   | `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
   | `AWS_REGION` | e.g. `us-east-1` |
   | `AWS_ECR_LOGIN_URI` | ECR registry URI (without repo name) |
   | `ECR_REPOSITORY_NAME` | Name of the ECR repository |

Once configured, pushes to the main branch trigger the workflow, which builds, pushes, and redeploys the app automatically.

## Development Workflow

When extending the pipeline (e.g., adding a new stage or changing behavior), the recommended order is:

1. Update `config/config.yaml`
2. Update `secrets.yaml` *(optional, for credentials)*
3. Update `params.yaml`
4. Update the relevant entity in `src/cnnclassifier/entity`
5. Update `ConfigurationManager` in `src/cnnclassifier/config`
6. Update the relevant component in `src/cnnclassifier/components`
7. Update the pipeline in `src/cnnclassifier/pipeline`
8. Update `main.py`
9. Update `dvc.yaml`
10. Update `app.py` if the change affects serving/inference

---

### Contributing

Issues and PRs are welcome — whether that's improving model performance, cleaning up the pipeline code, or extending the deployment setup.