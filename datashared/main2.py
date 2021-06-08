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

movieDF = spark.read.format("csv").option("header", "true").option("encoding", "UTF-8").load("hdfs://master:9000/data/220kmovies.csv")

certRDD = movieDF.select("certificate").filter(movieDF.certificate != '').rdd
certPairRDD = certRDD.flatMap(lambda x: x).map(lambda x: (x, 1)).reduceByKey(lambda x,y: x+y).sortBy(lambda x: x[1], ascending=False)

allCertKeys = certPairRDD.keys().collect()
allCertValues = certPairRDD.values().collect()

otherKey = "Other"
otherValue = 0
for i in allCertValues[6:]:
    otherValue += i

certKeys = allCertKeys[:6]
certKeys.append(otherKey)

certValues = allCertValues[:6]
certValues.append(otherValue)

plt.pie(certValues, labels = certKeys, startangle=90, autopct='%1.1f%%')
plt.savefig("/datashared/figure2.png")