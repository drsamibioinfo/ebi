FROM ubuntu

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.8 python3-pip python3.8-dev

COPY docker.txt .

RUN cat docker.txt | xargs -n1 pip3 install

COPY restful.py /usr/bin/restful

RUN chmod a+x /usr/bin/restful

CMD ["/usr/bin/restful"]