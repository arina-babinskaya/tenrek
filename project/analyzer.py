from metrics import cyclomatic
from metrics import nesting

class ComplexityAnalyzer:
    def __init__(self, parser):
        self.parser = parser

    def analyze(self):
        results = []

        functions = self.parser.get_functions()

        for func in functions:
            info = self.parser.get_function_info(func)

            cc = cyclomatic.calculate(func)
            nest = nesting.calculate(func)

            result = {
                **info,
                "cyclomatic_complexity": cc,
                "max_nesting_depth": nest,
                "loc": info["end_line"] - info["start_line"] + 1
            }

            results.append(result)

        return results



    


