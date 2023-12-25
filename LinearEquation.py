import numpy as np
import re

def getMaxNumberOfLhsAndRhsCoef(equations):
    maxCountLhs = 0
    maxCountRhs = 0
    for equation in equations:
        lhs_matches = re.findall(r'([+-]?\s*\d*)[a-zA-Z]?\s*', equation.split('=')[0])
        rhs_matches = re.findall(r'([+-]?\s*\d*)[a-zA-Z]?\s*', equation.split('=')[1])

        # Convert the coefficients to integers and create matrices
        lhs_coefficients = [int(match.replace(' ', '')) if match.strip() else 0 for match in lhs_matches]
        rhs_constant = [int(match.replace(' ', '')) if match.strip() else 0 for match in rhs_matches]

        lhs_coefficients.pop()
        rhs_constant.pop()

        if(len(lhs_coefficients) > maxCountLhs):
            maxCountLhs = len(lhs_coefficients)

        if(len(rhs_constant) > maxCountRhs):
            maxCountRhs = rhs_constant

    return [maxCountLhs, maxCountRhs]
def solveLinearEquation(equations):
    # numberOfCoef = getMaxNumberOfLhsAndRhsCoef(equations[0])

    lhsEquationArray = []
    rhsEquationArray = []

    for equation in equations:
        lhs_matches = re.findall(r'([+-]?\s*\d*)[a-zA-Z]?\s*', equation.split('=')[0])
        rhs_matches = re.findall(r'([+-]?\s*\d*)[a-zA-Z]?\s*', equation.split('=')[1])

        # Convert the coefficients to integers and create matrices
        lhs_coefficients = [int(match.replace(' ', '')) if match.strip() else 0 for match in lhs_matches]
        rhs_constant = [int(match.replace(' ', '')) if match.strip() else 0 for match in rhs_matches]

        lhs_coefficients.pop()
        rhs_constant.pop()

        lhsEquationArray.append(lhs_coefficients)
        rhsEquationArray.append(rhs_constant)

        lhs_matrix = np.vstack(lhsEquationArray)
        rhs_matrix = np.vstack(rhsEquationArray)

    print(lhs_matrix)
    print(rhs_matrix)
    result = []
    X = np.linalg.solve(lhs_matrix, rhs_matrix)
    print(X)
    for value in X:
        result.append(value[0])

    return result