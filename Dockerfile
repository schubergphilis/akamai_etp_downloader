FROM python:3.7-slim

RUN apt-get update
ENV INSTALLDIR=/opt/akamaietp_downloader
COPY * $INSTALLDIR/
WORKDIR $INSTALLDIR/
RUN pip install -r requirements.txt
ENTRYPOINT ["./docker-entrypoint.sh"]
