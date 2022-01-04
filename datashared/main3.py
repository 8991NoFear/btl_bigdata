import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark import SparkConf

conf = SparkConf()
conf.setMaster('spark://master:7077')
conf.setAppName('RHUST')

sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")

spark = SparkSession(sc)
movieDF = spark.read.format("csv").option("header", "true").option("encoding", "UTF-8").load("hdfs://master:9000/data/6kmovies.csv")

ratingRDD = movieDF.select("rating").filter(movieDF.rating != '').rdd

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

ratings = ratingRDD.flatMap(lambda x: x).filter(lambda x: isfloat(x)).collect()
for i in range(len(ratings)):
    ratings[i] = float(ratings[i])

bins = [x/10 for x in range(101)]
plt.xlabel("points")
plt.ylabel("films")
plt.title("rating point spectrum")
plt.hist(ratings, bins, color="g")
plt.savefig("/datashared/figure3.png")