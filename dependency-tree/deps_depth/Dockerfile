FROM python:3.5
FROM node:8

RUN groupadd -r analysis && useradd -m --no-log-init --gid analysis analysis
RUN npm install npm-remote-ls -g
RUN npm install -g npm-install-missing
USER analysis
COPY src /analyzer

WORKDIR /
CMD ["/analyzer/analyze.sh"]
