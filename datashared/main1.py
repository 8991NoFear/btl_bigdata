# import numpy as np
# import os
# import matplotlib.pyplot as plt
# packages = "org.apache.spark:spark-sql_2.12:3.0.1"
# os.environ["PYSPARK_SUBMIT_ARGS"] = (
# "--packages {0} pyspark-shell".format(packages)
# )

# import matplotlib
# matplotlib.use('TkAgg') # apt install python3-tk
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np

from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql import SQLContext
from pyspark import SparkConf

conf = SparkConf()
conf.setMaster('spark://master:7077')
conf.setAppName('RHUST')

sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")

spark = SparkSession(sc)

movieDF = spark.read.format("csv").option("header", "true").option("encoding", "UTF-8").load("hdfs:///dataset/dataset02/220kmovies.csv")

directorRDD = movieDF.select("director").filter(movieDF.director != '').rdd
directorRDD = directorRDD.flatMap(lambda x: x)
directorPairRDD = directorRDD.map(lambda x: (x, 1))
directorPairRDD = directorPairRDD.reduceByKey(lambda x,y: x+y).sortBy(lambda x: x[1], ascending=True)

directorKeys = directorPairRDD.keys().collect()
directorValues = directorPairRDD.values().collect()

figure(figsize=(16, 9))
plt.grid(axis="x")
plt.xlabel("film")
plt.ylabel("director")
plt.title("top 11 director by number of film produced")

plt.barh(directorKeys[-11:], directorValues[-11:])
plt.savefig("/datashared/figure1.png")