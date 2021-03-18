FROM python:3.9-alpine
LABEL maintainer="Ian Spence <ian@ecn.io>"
LABEL org.opencontainers.image.source=https://github.com/ecnepsnai/cfdosync
ADD [ "sync.py", "requirements.txt", "." ]
RUN pip install --no-cache-dir -r requirements.txt
ENV FIREWALL_ID=""
ENV API_KEY=""
CMD [ "python", "sync.py" ]