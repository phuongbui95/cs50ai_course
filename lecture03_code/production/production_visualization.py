import numpy as np
import matplotlib.pyplot as plt

# Create a range of x1 values
x1_vals = np.linspace(0, 10, 500)

# Constraint 1: 5x1 + 2x2 = 20 → x2 = (20 - 5x1)/2
x2_c1 = (20 - 5*x1_vals) / 2

# Constraint 2: 5x1 + 6x2 = 45 → x2 = (45 - 5x1)/6
x2_c2 = (45 - 5*x1_vals) / 6

# Plot constraints
plt.plot(x1_vals, x2_c1, label='5x₁ + 2x₂ = 20', color='blue')
plt.plot(x1_vals, x2_c2, label='5x₁ + 6x₂ = 45', color='red')

# Shade feasible region
# We'll test points below both lines:
x1 = []
x2 = []

for x in np.linspace(0, 10, 200):
    for y in np.linspace(0, 12, 200):
        if (5*x + 2*y <= 20) and (5*x + 6*y >= 45):
            x1.append(x)
            x2.append(y)

plt.scatter(x1, x2, color='lightgreen', s=2, label='Feasible Region')

# Plot optimal point
plt.plot(1.5, 6.25, 'ko', markersize=8, label='Optimal Point (1.5, 6.25)')

plt.xlim(0, 10)
plt.ylim(0, 12)
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.title('Linear Programming Constraints and Feasible Region')
plt.legend()
plt.grid(True)
plt.show()
