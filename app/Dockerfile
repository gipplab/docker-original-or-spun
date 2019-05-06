FROM ubuntu:latest
LABEL maintainer="Tomas Foltynek, foltynek@uni-wuppertal.de"
RUN apt-get update -y \
    && apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
EXPOSE 5000