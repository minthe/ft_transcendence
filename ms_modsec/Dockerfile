FROM owasp/modsecurity:nginx

COPY ./html /usr/share/nginx
COPY ./nginx_start.sh /nginx_start.sh

RUN touch /var/log/modsec_audit.log && \
    chmod 666 /var/log/modsec_audit.log

RUN mkdir -p /opt/modsecurity/var/log/ && \
    touch /opt/modsecurity/var/log/debug.log && \
    chmod 666 /opt/modsecurity/var/log/debug.log

CMD ["/nginx_start.sh"]
