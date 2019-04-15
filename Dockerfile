FROM registry.centos.org/centos/centos:7

ENV LANG=en_US.UTF-8

RUN yum install -y epel-release &&\
    yum install -y gcc python36-pip python36-devel &&\
    yum clean all

RUN mkdir -p /api_gateway/gateway

COPY gateway/* /api_gateway/gateway/

COPY requirements.txt /api_gateway/

ADD scripts/entrypoint.sh /bin/entrypoint.sh

RUN pip3 install --upgrade pip && pip install --upgrade wheel && \
    pip3 install -r /api_gateway/requirements.txt

WORKDIR /api_gateway/gateway

CMD ["/bin/entrypoint.sh"]
