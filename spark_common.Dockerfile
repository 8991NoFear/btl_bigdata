FROM ubuntu:18.04

RUN apt update && apt install vim curl -y 

RUN apt install openjdk-8-jdk -y

RUN apt install scala -y

RUN apt install python3 -y

RUN apt install python3-pip -y

RUN python3 -m pip install -U pip

RUN python3 -m pip install -U matplotlib

RUN apt install ssh openssh-server -y

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

RUN chmod 0600 ~/.ssh/authorized_keys

COPY ./conf/ssh/sshd_config /etc/ssh/

WORKDIR /opt

RUN curl https://dlcdn.apache.org/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz -o hadoop-3.2.2.tar.gz

RUN tar -xvzf hadoop-3.2.2.tar.gz

RUN rm -rf hadoop-3.2.2.tar.gz

COPY ./conf/hadoop/core-site.xml /opt/hadoop-3.2.2/etc/hadoop/

COPY ./conf/hadoop/hadoop-env.sh /opt/hadoop-3.2.2/etc/hadoop/

COPY ./conf/hadoop/hdfs-site.xml /opt/hadoop-3.2.2/etc/hadoop/

COPY ./conf/hadoop/workers /opt/hadoop-3.2.2/etc/hadoop/

ENV HADOOP_HOME="/opt/hadoop-3.2.2"

ENV PATH="${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin"

RUN hdfs namenode -format

WORKDIR /opt

RUN curl https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz -o spark-3.1.2-bin-hadoop3.2.tgz

RUN tar -xvzf spark-3.1.2-bin-hadoop3.2.tgz

RUN rm -rf spark-3.1.2-bin-hadoop3.2.tgz

ENV SPARK_HOME="/opt/spark-3.1.2-bin-hadoop3.2"

ENV PATH="${PATH}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin"

ENV PYSPARK_PYTHON="/usr/bin/python3"

ENTRYPOINT service ssh restart && bash
