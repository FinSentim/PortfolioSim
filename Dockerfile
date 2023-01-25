FROM python:3.10

# Set the working directory
WORKDIR /portfolio_sim

RUN apt-get update && apt-get -y upgrade
RUN python -m pip install --upgrade pip

# Install requirements
COPY ./requirements_dev.txt /portfolio_sim
RUN python -m pip install --no-cache-dir -r requirements_dev.txt
