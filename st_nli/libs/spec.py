class Spec:
    def __init__(self, filters=[]):
        self.filters = filters
        self.selectors = []
    def integrate_obj_spec(self, obj):
        if "filters" in obj:
            self.filters.extend(obj['filters'])
    def extend_selectors(self, selectors):
        self.selectors.extend(selectors)
def merge_specs(a, b):
    spec = {
        "filters": []
    }
    if "filters" in a:
        spec['filters'].extend(a['filters'])
    if "filters" in b:
        spec['filters'].extend(b['filters'])
    return spec
