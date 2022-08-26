# Fastidius


Fastidius is a CLI tool for creating [FastAPI](https://fastapi.tiangolo.com) backends, with integrations for deploying to DigitalOcean via Github Actions.


## Installation

```
pip install fastidius
```

## Usage

To initialize a new project, run

```
fastidius create
```

This will take you through a few setup instructions, then you'll have a fully fledged FastAPI
application ready to go.


## Deploying the API on DigitalOcean

Fastidius's real strength lies in it's quick deploy capability for DigitalOcean.

It's currently set up to use Ubunutu droplets. Once you've spin up a brand
new droplet on your DigitalOcean account, run this command
```
export IP_ADDRESS=<Your droplet's IP>
fastidius initialize-server
```

This will generate another command for running the initializer – this will set up firewalls,
add a non-root user (ubuntu), set up docker, and a few other configurations.


Next, we configure caddy server.

```
fastidius configure-caddy
```

Caddy is an awesome replacement for Nginx or Traefik, with SSL out of the box and minimal boilerplate.
Fastidius will use the above command to set up a new docker container that will manage caddy.

After you've set up your Caddyfile, you can deploy it using
```
fastidius deploy-caddy
```

Next, we want to set up the secrets on Github. This will create a CI/CD pipeline automatically.
```
fastidius github-setup
```

Once this is all done, pushing to the main branch on github will deploy your API 😏
