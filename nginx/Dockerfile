FROM alpine:3.19.1

RUN apk update; apk upgrade; apk add nginx; apk add openssl; apk add --no-cache gettext

# RUN chmod +x ./nginx_setup.sh
COPY ./nginx_start.sh /nginx_start.sh
# EXPOSE 443
# ENTRYPOINT [ "sh", "/nginx_setup.sh" ]

# CMD ["nginx", "-g", "daemon off;"]
CMD ["/nginx_start.sh"]