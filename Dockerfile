FROM python:3.12-slim

COPY requirements.txt /
RUN pip install -U pip && pip install -r requirements.txt


COPY ./scripts /scripts

WORKDIR /

VOLUME /etis

ENTRYPOINT [ "python3" ]
CMD ["./scripts/extracao.py"]