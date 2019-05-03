* Python Project files in `/src`
* SSH Public Key / Config in `/ssh_config

This GitHub repository is automatically build into the Docker Hub Repository:
* https://cloud.docker.com/u/aggipp/repository/docker/aggipp/original-or-spun`

The image from the Docker Hub repository is then updated in 5min intervals onto our dke01 server.

Container configuration on dke01:
* port `5000` is exposed
* `/data` is a persistent volume
