###
#
##

FROM alpine:latest

LABEL maintainer="Mike Carey <mcarey@solstice.com>"

RUN apk update
RUN apk add python3
RUN rm -rf /var/cache/apk/*

COPY ./bin /srv/bin
COPY ./lib /srv/lib

WORKDIR /srv

ENTRYPOINT /srv/entrypoint.sh

# Dockerfile
