# A web app to recognize whether a text was machine-paraphrased
# https://cloud.docker.com/repository/docker/tfoltynek/original-or-spun
# Info on dockerfile: Since each command creates an intermediate image, statements that don't change over time
# should be stated first.

# We start of with a python 3 base image that is a more packed distribution
FROM python:3.7.3-slim-stretch
LABEL maintainer="Tomas Foltynek, foltynek@uni-wuppertal.de"

# Networkings
EXPOSE 5000

# Update before we can will up the image
# Install Open SSH and other useful networking tools.
RUN apt-get update -y \
    && apt-get install -y openssh-server curl dnsutils net-tools iputils-ping iproute2 jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && mkdir /var/run/sshd
# Set up automatic login as root for ssh sessions
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

# Install additional Python installations
#RUN apt-get update -y \
#    && apt-get install -y python3-sklearn

# Copy SSH keys for this container
RUN mkdir /root/.ssh
COPY ssh_config/authorized_keys /root/.ssh/authorized_keys
# Set permission right and SSH update
RUN chmod 600 /root/.ssh/authorized_keys

# Set a work dir inside the container and prepare python application requirements
# IMPORTANT: requirements file (not automatically detected by pip freeze: scikit-learn
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy application into the container
COPY src .


# Run SSH and the application
CMD /usr/sbin/sshd -E /var/log/ssh.log  && python app.py
