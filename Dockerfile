FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt update

RUN apt install -y wkhtmltopdf
RUN apt install -y wget
RUN apt install -y xfonts-base
RUN apt install -y xfonts-75dpi
RUN apt install -y gdal-bin python3-gdal libgdal-dev python3-pycurl
#RUN pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')>
RUN pip install -r requirements.txt