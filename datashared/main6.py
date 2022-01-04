import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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

genreRDD = movieDF.select("genre").filter(movieDF.genre != '').rdd
totalFilm = genreRDD.count()
genrePairRDD = genreRDD.flatMap(lambda x: x).flatMap(lambda x: x.split(",")).map(lambda x: (x, 1))
genrePairRDD = genrePairRDD.reduceByKey(lambda x,y: x+y).sortBy(lambda x: x[1], ascending=False)

allGenreKeys = genrePairRDD.keys().collect()
allGenreValues = genrePairRDD.values().collect()

otherKey = "Other"
otherValue = 0
for i in allGenreValues[8:]:
    otherValue += i

genreValues = allGenreValues[:8]
genreValues.append(otherValue)

genreKeys = allGenreKeys[:8]
genreKeys.append(otherKey)
for i in range(len(genreKeys)):
    genreKeys[i] = str(genreValues[i]) + str(" films ") + genreKeys[i]

fig, ax = plt.subplots(figsize=(16, 9), subplot_kw=dict(aspect="equal"))

wedges, texts = ax.pie(genreValues, wedgeprops=dict(width=0.5), startangle=90)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(genreKeys[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y), horizontalalignment=horizontalalignment, **kw)

ax.set_title("Genres of " + str(totalFilm)  + " films")

plt.show()
plt.savefig("/datashared/figure6.png")