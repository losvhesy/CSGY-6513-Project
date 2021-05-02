import altair as alt
from vega_datasets import data
from .parsers import Parser
from ..configs.spatial import spatial_commonsense
from ..configs.attrs import attr_configs
from ..configs import state2fips
from .selectors import AttrSelector
import pandas as pd
def process_nlq(sent, df):
    interface = NLInterface()
    return interface.run(sent, df)

class NLInterface:
    def __init__(self):
        self.parser = Parser(attr_configs, spatial_commonsense)

    def run(self, sent, df):
        print("input: ", sent)
        spec = self.parser.parse_sent(sent)
        selectors = NLInterface.build_selectors(spec.selectors)
        task = NLInterface.infer_task(spec)
        print("spec:", spec.filters)
        f = NLInterface.build_executor(task, selectors, spec.filters, "state")
        return f(df)

    @staticmethod
    def infer_task(spec):
        tfilters = list(filter(lambda x: x.type == "temporal", spec.filters))
        if len(tfilters) == 0:
            return "time-series"
        elif tfilters[0].op != "on":
            return "time-series"
        else:
            return "map"

    @staticmethod
    def build_selectors(attrs):
        selectors = []
        for attr in attrs:
            selector = AttrSelector(attr)
            selectors.append(selector)
        return selectors

    @staticmethod
    def build_executor(task, selectors, filters, group):
        def f(df):
            selector = selectors[0]
            for filter_inst in filters:
                df = filter_inst.run(df)
            source = df.toPandas()
            if task == "time-series":
                attrname = selector.get_attr()
                if group == "state":
                    line = alt.Chart(source).mark_line(interpolate='basis').encode(
                        x='date:T',
                        y='{}:Q'.format(attrname),
                        color='state:O',
                    ).properties(
                        width=300, height=300
                    )
                    return line
            elif task == "map":
                if True:
                    states_topo = alt.topo_feature(data.us_10m.url, 'states')
                    attrname = selector.get_attr()
                    source = pd.merge(source, state2fips, how='left',
                                      left_on='state', right_on='state')
                    return alt.Chart(source).mark_geoshape().encode(
                        shape='geo:G',
                        color='{}:Q'.format(attrname),
                        tooltip=['state:N', alt.Tooltip(attrname, format='.2f')],
                    ).transform_lookup(
                        lookup='fip',
                        from_=alt.LookupData(data=states_topo, key='id'),
                        as_='geo'
                    ).properties(
                        width=300,
                        height=175,
                    ).project(
                        type='albersUsa'
                    )

        return f
