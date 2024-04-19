FROM debian:stable-slim

USER root

RUN apt-get update && apt-get install bison build-essential ca-certificates curl dh-autoreconf doxygen \
    flex gawk git iputils-ping libcurl4-gnutls-dev libexpat1-dev libgeoip-dev liblmdb-dev \
    libpcre3-dev libssl-dev libtool libxml2 libxml2-dev libyajl-dev locales \
    liblua5.3-dev pkg-config wget zlib1g-dev zlib1g-dev libxslt1-dev libgd-dev \
    git -y

RUN cd /opt && git clone https://github.com/SpiderLabs/ModSecurity && \
    cd ModSecurity && \ 
    git submodule init && \
    git submodule update && \
    ./build.sh && \
    ./configure && \
    make && \
    make install



# Downloading ModSecurity-Nginx Connector

RUN cd /opt && git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git && \
    wget http://nginx.org/download/nginx-1.22.1.tar.gz && \
    tar -xvzmf nginx-1.22.1.tar.gz 

COPY ./get_modules.sh /opt/nginx-1.22.1

# install nginx to make the binary ready for the script

RUN apt-get update && apt-get install -y nginx

RUN cd /opt/nginx-1.22.1 && \
    chmod 777 get_modules.sh && \
    ./get_modules.sh

RUN cd /opt/nginx-1.22.1 && make modules && \
    mkdir /etc/nginx/modules && \
    cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules && \
    cd conf && rm -f nginx.conf

COPY nginx.conf /opt/nginx-1.22.1/conf/nginx.conf

# Setting Up OWASP-CRS

RUN rm -rf /usr/share/modsecurity-crs && \
    git clone https://github.com/coreruleset/coreruleset /usr/local/modsecurity-crs && \
    mv /usr/local/modsecurity-crs/crs-setup.conf.example /usr/local/modsecurity-crs/crs-setup.conf && \
    mv /usr/local/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example /usr/local/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf 

# Configuring Modsecurity  

RUN mkdir -p /etc/nginx/modsec && \
    cp /opt/ModSecurity/unicode.mapping /etc/nginx/modsec && \
    rm -f ../sites-available/default

# Configure Nginx

COPY mod_security.conf /etc/nginx/modsec/mod_security.conf
COPY main.conf  /etc/nginx/modsec/main.conf
COPY Makefile .
COPY default /etc/nginx/sites-available/default

EXPOSE 8081

 CMD ["nginx", "-g", "daemon off;"]


