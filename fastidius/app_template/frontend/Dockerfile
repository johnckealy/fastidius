FROM node:latest

USER root

RUN yarn global add @quasar/cli

RUN mkdir /frontend
WORKDIR /frontend

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN yarn install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .
