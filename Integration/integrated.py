#!/usr/bin/env python

from pyspark.sql import SparkSession
from pyspark.sql.functions import format_string
import sys

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()


m = spark.read.format('csv').options(header='true',inferschema='true').load( "/user/sj3358/state_mobility.csv" )                                                                         
s = spark.read.format('csv').options(header='true',inferschema='true').load( "/user/sj3358/us-states.csv" )

m.createOrReplaceTempView("m")
s.createOrReplaceTempView("s")


result = spark.sql("SELECT m.date, m.country_region, m.sub_region_1 as state, m.place_id, m.retail_and_recreation_percent_change_from_baseline, \
                         m.grocery_and_pharmacy_percent_change_from_baseline, m.parks_percent_change_from_baseline, \
                         m.transit_stations_percent_change_from_baseline , m.workplaces_percent_change_from_baseline, \
                         m.residential_percent_change_from_baseline, s.cases, s.deaths \
                    FROM m, s WHERE m.date = s.date and m.sub_region_1 = s.state")

result.write.save("project1.csv",format="csv", header = True)
