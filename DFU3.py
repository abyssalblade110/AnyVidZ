def handle_invalid_order():
    """
    Function to handle invalid orders.
    """
    print("Order is invalid. Please check the details.")

def handle_empty_order():
    """
    Function to handle orders with no items.
    """
    print("Order is empty. Add items before proceeding.")

def handle_payment_failure():
    """
    Function to handle payment failures.
    """
    print("Payment was unsuccessful. Please try again.")

def process_shipping(order):
    """
    Function to process the shipping of a valid and successfully paid order.
    """
    print(f"Processing shipping for order: {order}")

# Chained Conditionals Example

def check_value(x):
    """
    Chained Conditionals involve using a sequence of if, elif, and else statements.
    Each condition is checked sequentially. Once a condition is met, its block is executed,
    and the rest are skipped.
    This approach is useful when only one condition needs to be true to execute a block of code.
    """
    if x > 10:
        return "Value is greater than 10"
    elif x == 10:
        return "Value is exactly 10"
    else:
        return "Value is less than 10"

print(check_value(15))  # Output: Value is greater than 10

# Nested Conditionals Example

def classify_number(x):
    """
    Nested Conditionals occur when one conditional statement is placed inside another.
    This approach is useful when multiple layers of logic need to be evaluated.
    Here, classify_number uses nested conditionals to determine the classification of the number
    based on its value.
    """
    if x >= 0:
        if x == 0:
            return "Zero"
        elif x > 0:
            if x < 10:
                return "Single digit positive"
            else:
                return "Positive number greater than 9"
    else:
        return "Negative number"

print(classify_number(7))  # Output: Single digit positive

# Strategy to Avoid Deeply Nested Conditionals

def process_order(order):
    """
    Deeply nested conditionals can make code harder to read and maintain.
    A common strategy to avoid this is to use guard clauses.
    Guard clauses are early exits from a function or block of code that handle specific cases first,
    simplifying the remaining logic.
    
    Example of refactoring a deeply nested conditional using guard clauses:
    """
    # Original deeply nested conditional
    if order.is_valid():
        if order.has_items():
            if order.payment_successful():
                process_shipping(order)
            else:
                handle_payment_failure()
        else:
            handle_empty_order()
    else:
        handle_invalid_order()

    # Refactored using guard clauses
def process_order(order):
    """
    Refactored process_order function that uses guard clauses to handle specific cases first,
    reducing the complexity of nested conditionals.
    """
    if not order.is_valid():
        handle_invalid_order()
        return
    if not order.has_items():
        handle_empty_order()
        return
    if not order.payment_successful():
        handle_payment_failure()
        return

    process_shipping(order)

# The guard clauses handle the specific cases early and simplify the remaining logic by ensuring
# that the conditions are checked in a straightforward manner.

# Discussion Question
"""
In what scenarios might using nested conditionals be more appropriate than using chained conditionals, despite the potential for reduced readability? Can you provide an example from your own programming experience?
"""
