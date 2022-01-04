Muốn truy cập vào container thì chạy lệnh sau: docker exec -ti [tên container] bash

0. crawl du lieu
- mo project imdb
- dung tai imdb_crawler chay lenh: scrapy crawl movie -o 6kmovies.csv -t csv
- di chuyen file crawl duoc vao thu muc datashared

1. chạy hdfs
chỉ truy cập vào container master và thực hiện:
- chạy lệnh: start-dfs.sh
- mở trình duyệt tại localhost:9870 kiểm tra đủ 2 datanode chưa

2. chạy spark
- truy cập vào container master và chạy lệnh: start-master.sh
- truy cập vào từng container worker và chạy lệnh: start-worker.sh spark://master:7077
- mở trình duyệt tại localhost:8080 kiểm tra đủ 2 workernode chưa

3. đẩy file vào hdfs
chỉ truy cập vào container master và thực hiện
- tạo một thư mục: hdfs dfs -mkdir /data
- đẩy file vào thư mục này: hdfs dfs -copyFromLocal /datashared/*.csv /data

4. submit jobs
spark-submit /datashared/main*.py --master http://master:7077

CHÚC BẠN MAY MẮN