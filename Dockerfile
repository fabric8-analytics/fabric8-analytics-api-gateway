FROM registry.centos.org/centos/centos:7

ENV LANG=en_US.UTF-8

RUN yum install -y epel-release &&\
    yum install -y gcc patch git python34-pip python34-requests httpd httpd-devel python34-devel postgresql-devel redhat-rpm-config libxml2-devel libxslt-devel python34-pycurl &&\
    yum clean all

RUN pip3 install -r requirements.txt && \

RUN mkdir -p /api_gateway

COPY gateway/* /api_gateway

RUN pip3 install --upgrade pip && pip install --upgrade wheel && \
    pip3 install -r /api_gateway/requirements.txt

WORKDIR /api_gateway

CMD python3 api_v1.py
