FROM alpine:3.19.1

RUN apk update; apk upgrade; apk add nginx; apk add openssl; apk add --no-cache gettext

COPY ./nginx_start.sh /nginx_start.sh

# EXPOSE 4242

CMD ["/nginx_start.sh"]
