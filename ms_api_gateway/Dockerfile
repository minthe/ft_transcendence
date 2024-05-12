FROM alpine:3.19.1

RUN apk update; apk upgrade; apk add nginx; apk add openssl; apk add --no-cache gettext

WORKDIR /usr/share/nginx/html
COPY ./html .

COPY ./nginx_start.sh /nginx_start.sh

CMD ["/nginx_start.sh"]