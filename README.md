# Original or spun?

## Project
* Python Project files in `/src`

## Container / Server Setup

### Important Information

* All data (installations, uploads, changes) in this container is volatile and
 will be reset to the state as described in the Dockerfile for each new deployment.
* If you want permanent changes e.g. another program installed or a different program
 setup. Please make your changes inside the `Dockerfile`.
* **Persistent data** across a deployment step is only guaranteed inside the mounted
 directory `/data`.

### Access

To login please copy your SSH public key into `/ssh_config/authorized_keys`.

* SSH access via 132.195.228.232
* Website via https://spun.w.ckurs.de/ (port 5000 forwarded) 

### CI Pipeline

This project is automatically build and pushed onto our university server.

* Docker Hub Repository _(access for ag-gipp members)_: \
 https://cloud.docker.com/u/aggipp/repository/docker/aggipp/original-or-spun

The deployment onto the server takes about 20 min in total, mostly depending 
on Docker Hub's performance.

1. Push Changes > GitHub (manual, whatever we code)
1. GitHub > Docker Hub (automatic, build pipeline of docker image)
2. Docker Hub > DKE Server (automatic, pull onto server via watchtower) 

Newer images from the Docker Hub repository are checked in 5min intervals.
