from metrics import cyclomatic
from metrics import nesting
from metrics import loc
from metrics.halstead import halstead_uniq_elements
from metrics.halstead import halstead_all_elements
from metrics.halstead import halstead_volume
from metrics.halstead import halstead_difficulty
from metrics.halstead import halstead_effort
from metrics.halstead import halstead_time

class ComplexityAnalyzer:
    def __init__(self, parser):
        self.parser = parser

    def analyze(self):
        results = []
        metrics = [
            cyclomatic,
            nesting,
            loc,
            halstead_uniq_elements,
            halstead_all_elements,
            halstead_volume,
            halstead_difficulty,
            halstead_effort,
            halstead_time
        ]

        functions = self.parser.get_functions()

        for func in functions:
            info = self.parser.get_function_info(func)
            result = { **info }

            for metric in metrics:
                name = metric.__name__.split('.')[-1]
                result[name] = metric.calculate(func)

            results.append(result)

        return results



    


