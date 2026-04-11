#returns a set of values
# in future: add possibility to make personalized comments about input format
from typing import List

def normalize_type(t: str) -> str:
    t = t.replace("const", "").replace("&", "").replace("*", "")
    return " ".join(t.split())

def get_values(arg_type: str) -> List[str]:
    base_type = normalize_type(arg_type)

    if base_type in {"int"}:
        return ["0", "1", "-1", "42", str(2**31 - 1), str(-2**31)]
    if base_type in {"short"}:
        return ["0", "1", "-1", "42", str(2**15 - 1), str(-2**15)]
    if base_type in {"long long"}:
        return ["0", "1", "-1", "42", str(2**63 - 1), str(-2**63)]
    
    if base_type in {"unsigned int"}:
        return ["0", "1", "42", str(2**32 - 1)]
    if base_type in {"unsigned long"}:
        return ["0", "1", "42", str(2**64 - 1)]
    
    if base_type in {"float"}:
        return ["0.0", "1.0", "-1.0", "3.14", "3.4e38", "-3.4e38"]
    if base_type in {"double"}:
        return ["0.0", "1.0", "-1.0", "3.14", "1.7e308", "-1.7e308"]
    
    if base_type == "bool":
        return ["true", "false"]
    
    if base_type == "char" :
        return ["'a'", "'\\0'", "'Z'", "'\\x7F'"]
    if base_type in {"std::string", "string"}:
        return ['""', '"test"', '"a"*1000']
    
    if "*" in arg_type:
        return ["nullptr"]

    return [f"/*UNKNOWEN_TYPE:{base_type}*/"]
