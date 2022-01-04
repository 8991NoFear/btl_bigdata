import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure
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

mPairRDD = movieDF.select("rating", "metascore").filter((movieDF.rating != '') & (movieDF.metascore != '')).rdd

mRatings = mPairRDD.keys().collect()
mMetascores = mPairRDD.values().collect()

for i in range(len(mRatings)):
    mRatings[i] = float(mRatings[i])
    
for i in range(len(mMetascores)):
    mMetascores[i] = int(mMetascores[i])

plt.xlabel("rating point")
plt.ylabel("metascore")
plt.title("rating-metascore scattering")

plt.scatter(mRatings, mMetascores, color='orange')
plt.savefig("/datashared/figure5.png")
