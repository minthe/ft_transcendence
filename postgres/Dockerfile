FROM postgres:16.2-alpine3.19

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=123
ENV POSTGRES_DB=postgres

COPY set_env.sh .
COPY entrypoint.sh .
COPY create_vault_cli.sh .
COPY postgressql.conf .

# RUN export postgres_user=$(vault read -format=json secret/data/POSTGRES_USER | jq -r '.data.data.POSTGRES_USER')
# RUN export postgres_password=$(vault read -format=json secret/data/POSTGRES_PASSWORD | jq -r '.data.data.POSTGRES_PASSWORD')
# RUN export postgres_port=$(vault read -format=json secret/data/POSTGRES_PORT | jq -r '.data.data.POSTGRES_PORT')
# RUN export postgres_db=$(vault read -format=json secret/data/POSTGRES_DB | jq -r '.data.data.POSTGRES_DB')

# ENV POSTGRES_USER=$postgres_user
# ENV POSTGRES_PASSWORD=$postgres_password
# ENV POSTGRES_PORT=$postgres_port
# ENV POSTGRES_DB=$postgres_db
RUN chmod +x entrypoint.sh
RUN chmod +x create_vault_cli.sh
RUN chmod +x set_env.sh

RUN ./create_vault_cli.sh
RUN ./set_env.sh

# RUN mkdir -p /var/lib/postgresql/data && \
#     chown -R postgres:postgres /var/lib/postgresql/data && \
#     chmod 700 /var/lib/postgresql/data

# RUN mv postgressql.conf /var/lib/postgresql/data

EXPOSE 5432


# ENTRYPOINT ["./entrypoint.sh"]
# Run set_env.sh to set the environment variables

# Optionally, you can unset the environment variables here if you don't want them in the final container environment

CMD ["postgres"]

# Continue building your Docker image
