from heapq import heappop, heappush

from utils import aoc_input_file, extract_ints, read_file_str

# Puzzle description: https://adventofcode.com/2015/day/22

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    def parse(s):
        return extract_ints(s)[0]

    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return list(map(parse, input))


SPELLS = {
    "missile": 53,
    "drain": 73,
    "shield": 113,
    "poison": 173,
    "recharge": 229,
}


#  State:
#     (player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer)
#
#  Returns:
#     - (new_state, won, mana_spent)
#     - None if the spell is illegal or the player dies.
def simulate_round(state, spell, boss_damage, part2=False):
    hp, mana, boss_hp, shield, poison, recharge = state

    def apply_effects():
        nonlocal mana, boss_hp, shield, poison, recharge

        if poison:
            boss_hp -= 3
            poison -= 1

        if recharge:
            mana += 101
            recharge -= 1

        if shield:
            shield -= 1

    def current_state():
        return (hp, mana, boss_hp, shield, poison, recharge)

    # Player's turn
    if part2:
        hp -= 1
        if hp <= 0:
            return None

    apply_effects()

    # Boss may die before a spell is cast
    if boss_hp <= 0:
        return current_state(), True, 0

    cost = SPELLS[spell]

    # Check spell legality
    if mana < cost:
        return None

    # Check spell duplication
    if (
        (spell == "shield" and shield)
        or (spell == "poison" and poison)
        or (spell == "recharge" and recharge)
    ):
        return None

    # Cast spell
    mana -= cost

    match spell:
        case "missile":
            boss_hp -= 4
        case "drain":
            boss_hp -= 2
            hp += 2
        case "shield":
            shield = 6
        case "poison":
            poison = 6
        case "recharge":
            recharge = 5

    if boss_hp <= 0:
        return current_state(), True, cost

    # Boss's turn
    apply_effects()

    if boss_hp <= 0:
        return current_state(), True, cost

    armour = 7 if shield else 0
    hp -= max(1, boss_damage - armour)

    if hp <= 0:
        return None

    return current_state(), False, cost


# use dijkstra to find minimum mana
def solve(player_hp, player_mana, boss_hp, boss_damage, part2=False):
    initial_state = (player_hp, player_mana, boss_hp, 0, 0, 0)

    queue = [(0, initial_state)]
    best_cost = {initial_state: 0}
    best_win = float("inf")

    while queue:
        mana_spent, state = heappop(queue)

        # No remaining path can improve the best victory
        if mana_spent >= best_win:
            break

        # Ignore states reached more cheaply before
        if mana_spent > best_cost[state]:
            continue

        for spell in SPELLS:
            result = simulate_round(state, spell, boss_damage, part2)

            if result is None:
                continue

            new_state, won, cost = result
            new_cost = mana_spent + cost

            if new_cost >= best_win:
                continue

            if won:
                best_win = new_cost
                continue

            if new_cost < best_cost.get(new_state, float("inf")):
                best_cost[new_state] = new_cost
                heappush(queue, (new_cost, new_state))

    return best_win if best_win != float("inf") else None


def main():
    test_input = (10, 250, 13, 8)
    test_input2 = (10, 250, 14, 8)
    input = read_input("day22.txt")

    assert (res := solve(*test_input)) == 226, f"Actual: {res}"
    assert (res := solve(*test_input2)) == 641, f"Actual: {res}"

    print(f"Part 1 {solve(50, 500, *input)}")  # 1824
    print(f"Part 2 {solve(50, 500, *input, True)}")  # 1937


if __name__ == "__main__":
    main()
