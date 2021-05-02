import pyspark.sql.functions as F
from pyspark.ml.regression import LinearRegression
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
import tqdm
import pandas as pd
import numpy as np
mobility_metrics = [
    "retail_and_recreation_percent_change_from_baseline",
    "grocery_and_pharmacy_percent_change_from_baseline",
    "workplaces_percent_change_from_baseline",
    "residential_percent_change_from_baseline"
]

class SparkEngine:
    def __init__(self, session):
        self.spark = session

    def add_idx(self, df):
        return df.withColumn("idx", F.monotonically_increasing_id())

    def join_population(self, covid_data, populations):
        population_df = self.spark.createDataFrame(populations)
        df = covid_data.join(population_df, on=['state'], how='left')
        df = df.withColumn("cases_by_population", (F.col("cases") * 100000 / F.col("population")))
        df = df.withColumn("deaths_by_population", (F.col("deaths") * 100000 / F.col("population")))
        return df

    def generate_state_metric_corr(self, df, states, metrics=mobility_metrics):
        assembler = VectorAssembler(
            inputCols=["cases_by_population", "deaths_by_population"],
            outputCol="features"
        )
        state_metric_correlation = {}
        lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8, featuresCol='features')
        state_metric_correlation['state'] = states
        for metric in metrics:
            state_metric_correlation[metric + "_cases"] = []
            state_metric_correlation[metric + "_deaths"] = []
            for state in tqdm.tqdm(states, desc='processing ' + metric):
                state_df = df.filter(df.state == state)
                state_training = assembler.transform(state_df)
                state_training = state_training.withColumn("label", (F.col(metric)))
                state_model = lr.fit(state_training)
                state_metric_correlation[metric + "_cases"].append(state_model.coefficients[0])
                state_metric_correlation[metric + "_deaths"].append(state_model.coefficients[1])
        state_metric_correlation = pd.DataFrame(state_metric_correlation)
        return state_metric_correlation
