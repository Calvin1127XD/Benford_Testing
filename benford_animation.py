import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict
import numpy as np

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlabel('Digits')
ax.set_ylabel('Frequency')

digit_count = defaultdict(int)
digits = list(range(1, 10))

# Generate a sequence of numbers from 1 to 1000000
numbers = np.random.randint(1, 1000000, size=10000)

def animate(i):
    # Extract leading digit
    leading_digit = int(str(numbers[i])[0])
    digit_count[leading_digit] += 1

    # Calculate frequencies
    frequencies = [digit_count[digit] for digit in digits]

    # Clear current plot
    ax.clear()
    bars = ax.bar(digits, frequencies, tick_label=digits)

    # Add frequency labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + .05, yval, ha='center', va='bottom')

    # Update title
    ax.set_title(f'Frequency of Leading Digits (Current number: {numbers[i]})')

# Create animation, update 200 times per second (interval in ms)
ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 10000), repeat=False, interval=5)
plt.show()
