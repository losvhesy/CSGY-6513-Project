import pyspark.sql.functions as F


class Filter:
    def __init__(self):
        self.type = ""
    def run(self, df):
        raise NotImplementedError("Filter Class is not implemented")


class AttrFilter(Filter):
    def __init__(self, attrname, comp, value):
        super(AttrFilter, self).__init__()
        self.attrname = attrname
        self.comp = comp
        self.value = value
        self.type = "attr"

    def run(self, df):
        if self.comp == "larger":
            return df.filter(df[self.attrname] > value)
        elif self.comp == "smaller":
            return df.filter(df[self.attrname] < value)
        elif self.comp == "equal":
            return df.filter(df[self.attrname] == value)


class TemporalFilter:
    def __init__(self, conds):
        self.type = "temporal"
        self.conds = conds
        self.op = self.conds[0]['op']

    def run_cond(self, df, cond):
        if cond['op'] == "after":
            return df.filter(F.col("date") > F.lit(cond['date'].strftime("%Y-%m-%d 00:01")))
        elif cond['op'] == "on":
            return df.filter(F.col("date") == F.lit(cond['date'].strftime("%Y-%m-%d")))
        elif cond['op'] == "before":
            return df.filter(F.col("date") < F.lit(cond['date'].strftime("%Y-%m-%d")))

    def run(self, df):
        for cond in self.conds:
            df = self.run_cond(df, cond)
        return df


class SpatialFilter:
    def __init__(self, states):
        self.states = states
        self.type = "spatial"

    

    def run(self, df):
        return df.filter(F.col("state").isin(self.states))