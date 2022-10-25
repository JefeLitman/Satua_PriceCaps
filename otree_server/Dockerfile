FROM python:3.10
RUN mkdir /otree
WORKDIR /otree
RUN pip install \
    otree \
    psycopg2 \
    numpy \
    pandas
CMD ["sh", "-c", "sleep 10; otree prodserver 0.0.0.0:8000"]