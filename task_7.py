from random import randint

import matplotlib.pyplot as plt


ANALYTICAL = {
    2: 1 / 36,
    3: 2 / 36,
    4: 3 / 36,
    5: 4 / 36,
    6: 5 / 36,
    7: 6 / 36,
    8: 5 / 36,
    9: 4 / 36,
    10: 3 / 36,
    11: 2 / 36,
    12: 1 / 36,
}


def simulate_dice_rolls(rolls: int) -> dict[int, float]:
    """Estimate probabilities of two-dice sums using Monte Carlo simulation."""
    counts = {total: 0 for total in range(2, 13)}

    for _ in range(rolls):
        counts[randint(1, 6) + randint(1, 6)] += 1

    return {
        total: count / rolls
        for total, count in counts.items()
    }


def print_results(probabilities: dict[int, float], analytical: dict[int, float]) -> None:
    """Print Monte Carlo and analytical probabilities."""
    print(
        f"{'Sum':>3} "
        f"{'Monte Carlo':>14} "
        f"{'Analytical':>12} "
        f"{'Difference':>12}"
    )
    print("-" * 45)

    for total, probability in probabilities.items():
        difference = abs(probability - analytical[total])

        print(
            f"{total:>3} "
            f"{probability:>13.2%} "
            f"{analytical[total]:>11.2%} "
            f"{difference:>11.2%}"
        )


def plot_probabilities(
        probabilities: dict[int, float],
        analytical: dict[int, float],
        rolls: int,
) -> None:
    """Plot Monte Carlo and analytical probabilities for two-dice sums."""
    sums = list(probabilities)
    values = list(probabilities.values())
    theory = [analytical[total] for total in sums]

    plt.figure(figsize=(10, 6))

    plt.bar(sums, values, tick_label=sums, label="Monte Carlo")

    plt.plot(sums, theory, color="red", linestyle="--", marker="o", label="Analytical")

    plt.xlabel("Dice sum")
    plt.ylabel("Probability")
    plt.title(f"Monte Carlo simulation — {rolls:,} rolls")

    for total, probability in probabilities.items():
        plt.text(total, probability, f"{probability:.2%}", ha="center", va="bottom")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    for rolls in (100, 1_000, 10_000, 100_000, 1_000_000):
        probabilities = simulate_dice_rolls(rolls)

        print(f"\n=== {rolls:,} rolls ===")
        print_results(probabilities, ANALYTICAL)

        plot_probabilities(probabilities, ANALYTICAL, rolls)
