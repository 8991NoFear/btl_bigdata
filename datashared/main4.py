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

yearRDD = movieDF.select("year").filter(movieDF.year != '').rdd
yearPairRDD = yearRDD.flatMap(lambda x: x).filter(lambda x: x.isnumeric()).map(lambda x: (x, 1))
yearPairRDD = yearPairRDD.reduceByKey(lambda x,y: x+y).sortBy(lambda x: x[0], ascending=True)

yearKeys = yearPairRDD.keys().collect()
yearValues = yearPairRDD.values().collect()

figure(figsize=(16, 9))
plt.xlabel("years")
plt.ylabel("films")
plt.title("film spectrum")
plt.grid(axis="y")

plt.bar(yearKeys[-21:], yearValues[-21:], width=0.5)
plt.savefig("/datashared/figure4.png")