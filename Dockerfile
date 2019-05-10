# A web app to recognize whether a text was machine-paraphrased
# https://cloud.docker.com/repository/docker/tfoltynek/original-or-spun
FROM ubuntu:latest
LABEL maintainer="Tomas Foltynek, foltynek@uni-wuppertal.de"
RUN apt-get update -y \
    && apt-get install -y python-pip python-dev build-essential

COPY src /app
WORKDIR /app
RUN pip install -r requirements.txt

#
# Update before we can will up the image
# Install Open SSH and other useful networking tools.
RUN apt-get update -y \
    && apt-get install -y openssh-server curl vim dnsutils net-tools iputils-ping iproute2 jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && mkdir /var/run/sshd
# Set up automatic login as root for ssh sessions
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
# Copy SSH keys for this container
RUN mkdir /root/.ssh
COPY ssh_config/authorized_keys /root/.ssh/authorized_keys
# Set permission right and SSH update
RUN chmod 600 /root/.ssh/authorized_keys
CMD /usr/sbin/sshd -D

# Run the python application
EXPOSE 5000
CMD ["python", "app.py"]
