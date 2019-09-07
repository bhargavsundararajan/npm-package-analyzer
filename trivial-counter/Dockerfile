FROM ubuntu:17.10
FROM node:8

COPY package.json /

RUN npm install 

RUN npm i escomplex --save \
    && npm install esprima

RUN groupadd -r analysis && useradd -m --no-log-init --gid analysis analysis

USER analysis
COPY src /analyzer

WORKDIR /
CMD ["/analyzer/analyze.sh"]
