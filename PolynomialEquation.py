import numpy as np
import re
import sympy as sp

def solvePolynomialEquation(equation):
    pattern1 = r'\((.*?)\)'
    input_string = equation.replace('=0', '').strip()
    match = re.search(pattern1, input_string)

    if match:
        content_inside_parentheses = match.group(1).strip()

        try:
            x_value = float(content_inside_parentheses)

            # Remove the content inside parentheses from the original equation
            equation_string_without_x = re.sub(pattern1, '', input_string).strip()

            print(f"The modified equation: {equation_string_without_x}")
            print(f"The extracted x value: {x_value}")
        except ValueError:
            print("Error: Unable to extract a valid x value.")
    else:
        print("Error: No content inside parentheses found.")

    modified_string = replace_variables_with_numbers(equation_string_without_x)
    final_string = add_asterisk_between_number_and_variable(modified_string)

    derivative = calculate_derivative(final_string)
    print(f"Derivative: {derivative}")

    root = newton_raphson_auto_initial_guess(final_string, x_value)
    return root

def replace_variables_with_numbers(input_string):
    def replace(match):
        return f'x**{match.group(1)}'

    modified_string = re.sub(r'x(\d+)', replace, input_string)
    return modified_string

def add_asterisk_between_number_and_variable(input_string):
    def add_asterisk(match):
        return f'{match.group(1)}*{match.group(2)}'

    modified_string = re.sub(r'(\d+)([a-zA-Z])', add_asterisk, input_string)
    return modified_string

def calculate_derivative(equation_str):
    try:
        x = sp.symbols('x')
        equation = sp.sympify(equation_str)

        derivative = sp.diff(equation, x)
        return derivative
    except sp.SympifyError:
        print("Invalid equation. Please enter a valid mathematical expression.")
        return None
def newton_raphson_auto_initial_guess(equation_str,guess, tol=1e-6, max_iter=100):
    x = sp.symbols('x')
    equation = sp.sympify(equation_str)

    # Calculate the derivative of the equation
    derivative = sp.diff(equation, x)

    # Automatic initial guess as the midpoint of the interval [a, b]


    # Define the functions using lambdify for numerical evaluation
    f = sp.lambdify(x, equation)
    df = sp.lambdify(x, derivative)

    # Newton-Raphson iteration

    iteration = 0

    while abs(f(guess)) > tol and iteration < max_iter:
        guess = guess - f(guess) / df(guess)
        iteration += 1

    if abs(f(guess)) <= tol:
        print(f"Root found at x = {guess} after {iteration} iterations.")
        return guess
    else:
        print("Newton-Raphson method did not converge with the specified initial guess.")
        return None
