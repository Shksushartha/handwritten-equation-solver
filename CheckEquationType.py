import re
def getEquationType(equation):
    linear_pattern = r'^\s*([+-]?\s*\d*\s*[a-zA-Z]?)\s*([+-]\s*\d*\s*[a-zA-Z]?)*\s*=\s*(\s*[+-]?\s*\d*\s*[a-zA-Z]?)\s*([+-]\s*\d*\s*[a-zA-Z]?)*$'

    # Check if the input matches the linear equation pattern
    if re.match(linear_pattern, equation):
        return 1 #linearEquation
    else:
        return 0