FROM alpine:3.19.1

RUN apk update; apk upgrade; apk add nginx; apk add openssl

COPY conf/nginx.conf /etc/nginx/nginx.conf

EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
