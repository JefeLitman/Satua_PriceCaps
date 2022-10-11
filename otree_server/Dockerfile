FROM python:3.10
RUN mkdir /otree
WORKDIR /otree
COPY . /otree/
RUN pip install -r requirements.txt
CMD ["sh", "-c", "sleep 10; otree prodserver 0.0.0.0:8000"]