FROM python:latest

RUN apt-get update -y && apt-get upgrade -y

# Set the working directory
WORKDIR /portfolio_sim

RUN python -m pip install --upgrade pip
RUN pip install ipykernel --upgrade

# Install requirements
COPY ./requirements_dev.txt /portfolio_sim
RUN python -m pip install --no-cache-dir -r requirements_dev.txt
