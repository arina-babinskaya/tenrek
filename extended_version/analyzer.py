#returns a set of values
# in future: add possibility to make personalized comments about input format
from typing import List

def get_values(arg_type: str) -> List[str]:
    base_type = arg_type.replace('&', '').replace('const', '').strip()

    if base_type in ["int", "short", "long"]:
        return ["0", "1", "-1"]
    if base_type in ["unsigned int", "unsigned long"]:
        return ["0", "1"]
    if base_type in ["float", "double"]:
        return ["0.0", "1.0", "-1.0"]
    if "bool" in base_type:
        return ["true", "false"]
    if "char" in base_type:
        return ["'a'", "'\\0'"]
    if "string" in base_type:
        return ['""', '"test"']
    return [f"/*stub:{base_type}*/"]
