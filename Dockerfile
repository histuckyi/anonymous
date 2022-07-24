FROM ubuntu:20.04

MAINTAINER Daim Tak <histuckyi@gmail.com>


ARG PYTHON_VERSION_TAG=3.10.5
ARG LINK_PYTHON_TO_PYTHON3=1

RUN apt-get -qq -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq -y install \
        gcc \
        g++ \
        zlibc \
        zlib1g-dev \
        libssl-dev \
        libbz2-dev \
        libsqlite3-dev \
        libncurses5-dev \
        libgdbm-dev \
        libgdbm-compat-dev \
        liblzma-dev \
        libreadline-dev \
        uuid-dev \
        libffi-dev \
        tk-dev \
        wget \
        curl \
        git \
        make \
        sudo \
        bash-completion \
        tree \
        vim \
        software-properties-common && \
    mv /usr/bin/lsb_release /usr/bin/lsb_release.bak && \
    apt-get -y autoclean && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt/lists/*


COPY install_python.sh install_python.sh
RUN bash install_python.sh ${PYTHON_VERSION_TAG} ${LINK_PYTHON_TO_PYTHON3} && \
    rm -r install_python.sh Python-${PYTHON_VERSION_TAG}

#RUN ln -s /usr/bin/python3 /usr/bin/python
#RUN python -m pip install pip --upgrade
#RUN python -m pip install wheel setuptools

RUN mkdir /code
WORKDIR /code
COPY requirements.txt ./requirements.txt
COPY entrypoint.sh ./entrypoint.sh
COPY gunicorn.py ./gunicorn.py
RUN pip install -r ./requirements.txt

COPY . ./
COPY .env.docker ./.env
RUN rm -rf ./wanted_backend/logs/*.log

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh

EXPOSE 7756