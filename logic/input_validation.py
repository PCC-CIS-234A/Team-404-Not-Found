import re


# Possible method for validating email user entries
# Check the format of an email entry using a regular expression
# from https://useful.codes/python-input-validation-and-sanitization/
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")


# Takes an input_type keyword argument.
# Executes an input validation function based on the input_type keyword.
# Takes optional parameters and passes them to the validation function.
# Returns the output from the validation function.
def input_item(input_type="int", *args, **kwargs):
    if input_type == "int":
        return input_int(*args, **kwargs)
    elif input_type == "float":
        return input_float(*args, **kwargs)
    elif input_type == "string":
        return input_string(*args, **kwargs)
    elif input_type == "y_or_n":
        return input_y_or_n(*args, **kwargs)
    elif input_type == "select_item":
        return select_item(*args, **kwargs)
    else:
        print("Error! Unknown type ", input_type)


# Tests that the number meets range parameters.
# Used in the input_int and input_float functions.
def number_in_range(value, ge, gt, le, lt):
    if ge is not None and value < ge:
        return False
    if gt is not None and value <= gt:
        return False
    if le is not None and value > le:
        return False
    if lt is not None and value >= lt:
        return False
    return True


# Asks the user to type a whole number.
# Validates user input and repeats until the user gives a valid answer.
# Takes optional keyword arguments to specify minimum and/or maximum values.
def input_int(
        prompt="Please enter a whole number: ",
        error="Input must be a whole number!",
        ge=None,
        gt=None,
        le=None,
        lt=None
):
    while True:
        try:
            val = int(input(prompt))
            if number_in_range(val, ge, gt, le, lt):
                return val
            print(error)
        except ValueError:
            print(error)


# Asks the user to type in a decimal number.
# Validates user input and repeats until the user gives a valid answer.
# Takes optional keyword arguments to specify minimum and/or maximum values.
def input_float(
        prompt="Please enter a decimal number: ",
        error="Input must be a decimal number!",
        ge=None,
        gt=None,
        le=None,
        lt=None
):
    while True:
        try:
            val = float(input(prompt))
            if number_in_range(val, ge, gt, le, lt):
                return val
            print(error)
        except ValueError:
            print(error)


# Asks the user to type in a piece of text.
# Validates user input and repeats until the user gives a valid answer.
# Takes an optional argument for a validation function.
# If no validation argument is provided, all non-empty input is valid.
def input_string(
        prompt="Please enter a string of text: ",
        error="Invalid must be non-empty!",
        valid=lambda s: len(s) > 0
):
    while True:
        try:
            val = input(prompt)
            if valid(val):
                return val
            print(error)
        except ValueError:
            print(error)


# Asks the user to answer a yes or no question.
# Validates user input and repeats until the user gives a valid answer.
# Variations of yes or no are included as valid responses.
# Returns True for yes and False for no.
def input_y_or_n(
        prompt="Please enter Yes or No: ",
        error="Input must be either Yes or No!"
):
    while True:
        val = input(prompt).lower()
        if val in ["y", "yes", "yep"]:
            return True
        if val in ["n", "no", "nope"]:
            return False
        print(error)


# Takes a list of choices and prompts the user to select a choice.
# Validates user input and repeats until the user gives a valid answer.
# Converts inputs to a consistent case.
# Takes an optional dictionary that maps possible inputs into specific outputs.
# Returns the choice that the user selected.
def select_item(
        choices=[],
        choice_map=None,
        prompt="Please select an item: ",
        error="Input must an item from the list!"
):
    value_dict = {}
    for choice in choices:
        value_dict[choice.lower()] = choice
    if choice_map is not None:
        for key in choice_map:
            value_dict[key.lower()] = choice_map[key]
    while True:
        val = input(prompt).lower()
        if val in value_dict:
            return value_dict[val]
        print(error)
