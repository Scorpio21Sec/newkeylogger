import random
def generate_random_numbers(n, start, end):
    """Generate a list of n random integers between start and end."""
    return [random.randint(start, end) for _ in range(n)]
print(generate_random_numbers(10, 1, 100))
generate_random_numbers(5, 10, 50)
# Note: This code 