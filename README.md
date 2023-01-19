# CoinHub -> Bigdata

## Install project

1. Install all package in file requirement.txt
   > pip install -r requirement.txt
2. Run docker
   > docker-compose up
   > If datanode crash to an error related to port, then change the port of datanode.
3. Enable safe mode in namenode
   > docker exec -it namenode /bin/bash R
   >
   > hdfs dfsadmin -safemode leave
   >
   > exit
4. Add hostname to C:\Windows\System32\drivers\etc\hosts.txt
   > 127.0.0.1 datanode-1
   >
   > 127.0.0.1 datanode-2
   >
   > 127.0.0.1 datanode-3
5. Add folder logs in folder consumer, producer

## Run

1. Run file producer
   > for /f %i in ('python -m certifi') do set SSL_CERT_FILE=%i
   >
   > python kafka/producer/app.py
2. Run file consumer
   > python kafka/consumer/app.py
