FROM python:3.10
RUN mkdir /otree
WORKDIR /otree
COPY ./* /otree/
RUN pip install -r requirements.txt
CMD otree devserver