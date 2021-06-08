muốn truy cập vào container thì chạy lệnh sau: docker exec -ti [tên container] bash

[do cau hinh yeu nen chi test mot container duy nhat vua lam master vua lam slave]

0. crawl du lieu
- mo project imdb
- dung tai imdb_crawler chay lenh: scrapy crawl movie -o 220kmovies.csv -t csv
- di chuyen file crawl duoc vao thu muc datashared/dataset2

1. chạy hdfs
chỉ truy cập vào container master và thực hiện:
- sửa file /home/hadoop-3.2.2/etc/hadoop/workers và liệt kê các container làm datanode
    e.g.
    worker1 
    worker2
- chạy lệnh: hdfs namenode -format
- chạy lệnh: start-dfs.sh
- mở trình duyệt tại localhost:9870 kiểm tra đủ 2 datanode chưa

2. chạy spark
- truy cập vào container master và chạy lệnh: start-master.sh
- truy cập vào từng container worker và chạy lệnh: start-worker.sh spark://master:7077
- mở trình duyệt tại localhost:8080

3. chạy zeppelin
chỉ truy cập vào container master và thực hiện:
- chạy lệnh: zeppelin-daemon.sh start
- mở trình duyệt tại localhost:8888 vào mục interpreter và uncheck thằng này zeppelin.spark.enableSupportedVersionCheck	sau đó lưu lại

4. đẩy file vào hdfs
chỉ truy cập vào container master và thực hiện
- tạo một thư mục: hdfs dfs -mkdir /data
- đẩy file vào thư mục này:
hdfs dfs -copyFromLocal /datashared/dataset01/*.csv /dataset/dataset01
hdfs dfs -copyFromLocal /datashared/dataset02/220kmovies.csv /dataset/dataset02

tạo 1 notebook trên zeppelin, copy code trong file datashared/main*.py ra, chinh sua và chạy. Trong lúc chạy có thể vào locahost:4040 để xem thông tin jobs

CHÚC BẠN MAY MẮN