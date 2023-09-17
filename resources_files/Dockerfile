#FROM container.repository.cloudera.com/cloudera/dex/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15
#FROM docker.repository.cloudera.com/cloudera/dex/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15

FROM docker-private.infra.cloudera.com/cloudera/dex/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15
USER root
RUN yum install ${YUM_OPTIONS} gcc openssl-devel libffi-devel bzip2-devel wget python39 python39-devel && yum clean all && rm -rf /var/cache/yum
RUN update-alternatives --remove-all python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.9 /usr/bin/python3
RUN yum install python39-pip
RUN /usr/bin/python3.9 -m pip install great_expectations==0.17.15
USER ${DEX_UID}
