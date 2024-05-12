FROM python:3.10.12
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt update -y
RUN apt install -y gdal-bin python3-gdal libgdal-dev python3-pycurl
#RUN pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}') --global-option=build_ext --global-option="-I/usr/include/gdal"
RUN pip install -r requirements.txt
#COPY . /code
