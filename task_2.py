import math
import sys

import matplotlib.pyplot as plt


def draw_branch(x: float, y: float, length: float, angle: float, depth: int) -> None:
    """Draw a Pythagoras tree recursively using line segments."""
    if depth == 0:
        return

    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)

    plt.plot([x, end_x], [y, end_y], color="firebrick")

    next_length = length / math.sqrt(2)
    branch_angle = math.pi / 4

    for sign in (1, -1):
        draw_branch(end_x, end_y, next_length, angle + branch_angle * sign, depth - 1)


if __name__ == "__main__":

    try:
        depth = int(sys.argv[1] if len(sys.argv) > 1 else input("Enter recursion depth: "))
    except ValueError:
        print("Recursion depth should be an integer")
    else:
        plt.figure(figsize=(8, 8))
        plt.axis("off")
        plt.axis("equal")

        draw_branch(
            x=0,
            y=0,
            length=100,
            angle=math.pi / 2,
            depth=depth,
        )

        plt.show()
