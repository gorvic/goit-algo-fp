menu = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}

Menu = dict[str, dict[str, int]]
Choice = tuple[int, int, list[str]]
Table = list[list[int | float]]

INFINITY = float("inf")  # Marks unreachable budget states in the DP table.


def greedy_algorithm(menu: Menu, budget: int) -> Choice:
    """Select food by the highest calories-to-cost ratio."""
    return _greedy_choice(menu, budget, reverse=True)


def greedy_algorithm_min(menu: Menu, budget: int) -> Choice:
    """Select food by the lowest calories-to-cost ratio."""
    return _greedy_choice(menu, budget, reverse=False)


def dynamic_programming(menu: Menu, budget: int) -> Choice:
    """Find the maximum-calorie choice using 0/1 knapsack."""
    foods, table = _build_dp_table(menu, budget, maximize=True)

    choice = _restore_choice(menu, foods, table, budget)
    total_cost = sum(menu[name]["cost"] for name in choice)

    return int(table[-1][budget]), total_cost, choice


def dynamic_programming_min(menu: Menu, budget: int) -> Choice:
    """Minimize calories while spending as much of the budget as possible."""
    foods, table = _build_dp_table(menu, budget, maximize=False)

    total_cost = next(
        cost
        for cost in range(budget, -1, -1)
        if table[-1][cost] != INFINITY
    )

    choice = _restore_choice(menu, foods, table, total_cost)

    return int(table[-1][total_cost]), total_cost, choice


def _greedy_choice(menu: Menu, budget: int, reverse: bool) -> Choice:
    """Select food greedily by calories-to-cost ratio."""
    calories = 0
    total_cost = 0
    choice = []

    ranked_menu = sorted(
        menu.items(),
        key=lambda item: item[1]["calories"] / item[1]["cost"],
        reverse=reverse,
    )

    for name, food in ranked_menu:
        if total_cost + food["cost"] <= budget:
            choice.append(name)
            total_cost += food["cost"]
            calories += food["calories"]

            if total_cost == budget:
                break

    return calories, total_cost, choice


def _build_dp_table(menu: Menu, budget: int, maximize: bool) -> tuple[list[str], Table]:
    """Build a 0/1 knapsack dynamic programming table."""
    foods = list(menu)
    best = max if maximize else min
    default = 0 if maximize else INFINITY

    table = [[default] * (budget + 1) for _ in range(len(foods) + 1)]

    if not maximize:
        table[0][0] = 0

    for row, name in enumerate(foods, 1):
        cost = menu[name]["cost"]
        calories = menu[name]["calories"]

        previous_row = table[row - 1]
        current_row = previous_row.copy()

        for limit in range(cost, budget + 1):
            current_row[limit] = best(
                previous_row[limit],
                previous_row[limit - cost] + calories,
            )

        table[row] = current_row

    return foods, table


def _restore_choice(menu: Menu, foods: list[str], table: Table, total_cost: int) -> list[str]:
    """Restore the selected food from a completed DP table."""
    choice = []
    remaining = total_cost

    for row in range(len(foods), 0, -1):
        if remaining == 0:
            break

        if table[row][remaining] == table[row - 1][remaining]:
            continue

        name = foods[row - 1]
        choice.append(name)
        remaining -= menu[name]["cost"]

    choice.reverse()

    return choice


def print_choice(title: str, result: Choice) -> None:
    """Print a food choice."""
    calories, total_cost, choice = result

    print(title)
    print(f"Calories: {calories}")
    print(f"Cost:     {total_cost}")
    print(f"Items:    {', '.join(choice)}")


if __name__ == "__main__":
    budget = 100

    print("=== Maximum calories ===")
    print_choice("\nGreedy algorithm:", greedy_algorithm(menu, budget))
    print_choice("\nDynamic programming:", dynamic_programming(menu, budget) )

    print("\n=== Minimum calories ===")
    print_choice("\nGreedy algorithm:", greedy_algorithm_min(menu, budget))
    print_choice("\nDynamic programming:", dynamic_programming_min(menu, budget))
