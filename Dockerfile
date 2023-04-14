
FROM python:3.9

RUN apt-get update
RUN apt-get -y install make

RUN mkdir /home/mnv3

COPY ./ /home/mnv3


WORKDIR /home/mnv3

RUN make install

ENTRYPOINT [ "gunicorn" ]

CMD [ "--bind", "0.0.0.0:8000", "wsgi:application" ]
