import re
def getEquationType(equation):
    calculation_pattern = r'^[0-9+\-*x/()]+$'

    linear_pattern = r'^(\s*[+-]?\s*\d*\s*[a-zA-Z])\s*(\s*[+-]\s*\d*\s*[a-zA-Z]\s*)*\s*=\s*([+-]?\s*\d*\s*)\s*$'

    quadratic_pattern = r'^(\s*[+-]?\s*(\d*)\s*([a-zA-Z])\s*(\^\s*(\d+))?)\s*(\s*[+-]\s*(\d*)\s*([a-zA-Z])\s*(\^\s*(\d+))?)*\s*=\s*([+-]?\s*\d*\s*)\s*$'

    # Check if the input matches the linear equation pattern
    if re.match(linear_pattern, equation):
        return 1 #linearEquation
    elif re.match(quadratic_pattern, equation):
        return 2 #linearEquation
    elif re.match(calculation_pattern, equation):
        return 3 #linearEquation
    else:
        return 0
