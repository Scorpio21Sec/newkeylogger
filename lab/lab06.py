import numpy as np

def temperature_conversion(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

print("\n===== TEMPERATURE CONVERSION TABLE =====")
print("Celsius\tFahrenheit")

# Use np.arange to generate Celsius values from 0 to 100 with step 10
celsius_values = np.arange(0, 101, 10)
fahrenheit_values = temperature_conversion(celsius_values)

for celsius, fahrenheit in zip(celsius_values, fahrenheit_values):
    print(f"{celsius}°C\t{fahrenheit}°F")
    if fahrenheit > 100:
        print("Warning: Temperature exceeds 100°F!")
    elif fahrenheit < 32:
        print("Warning: Temperature below freezing point!")

