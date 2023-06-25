![Linters](https://github.com/No-Code-DS/trainer/actions/workflows/tox.yml/badge.svg)
![Deployment](https://github.com/No-Code-DS/trainer/actions/workflows/docker-deploy.yml/badge.svg?branch=main)

# trainer

**Data Lume** service responsible for training a model after specific RabbitMQ event.

## Run locally

First Clone the project

```sh
# clone the repo
git clone https://github.com/No-Code-DS/trainer.git


# install requirements
cd trainer
pip install -r requirements.txt
# or
pip install .
```

prepare RabbitMQ connection

```sh
# set environment variable with connection string
export RABBIT_URL = "rabbitmq"
```

Start the service with:
```sh
python -u consumer.py
```
