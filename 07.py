from functools import cmp_to_key
from typing import List
from input_reader import read_input_from_file
from collections import Counter


CARD_VALUE = {k: v for v, k in enumerate("23456789TJQKA")}


# if left < right, return -1
# if right < left, return 1
# if left == right, return 0
def rank_hands(left: str, right: str):
    cards_count_left = Counter(left)
    cards_count_right = Counter(right)

    max_left = max(cards_count_left.values())
    max_right = max(cards_count_right.values())

    if max_left < max_right:
        return -1
    if max_left > max_right:
        return 1

    # possibilities left: 1) full house vs three of a kind   2) two pair vs 1 pair  3) same kind

    # handle 1) and 2)
    if max_left in (2, 3):
        # 1)
        #           if len(Counter(cards_count_left.keys())) == 3 -> three of a kind
        # otherwise if len(Counter(cards_count_left.keys())) == 2 -> full house (more powerful)
        if -len(Counter(cards_count_left.keys())) < -len(Counter(cards_count_right.keys())):
            return -1
        if -len(Counter(cards_count_left.keys())) > -len(Counter(cards_count_right.keys())):
            return 1

    # handle 3) same kind
    for card_idx in range(5):
        if CARD_VALUE[left[card_idx]] < CARD_VALUE[right[card_idx]]:
            return -1
        if CARD_VALUE[left[card_idx]] > CARD_VALUE[right[card_idx]]:
            return 1

    # they're the same hand
    return 0


def main(input_lines: List[str]):
    hands = {}
    for line in input_lines:
        hand = line.split()[0]
        bid = int(line.split()[1])
        hands[hand] = bid

    ranked_hands = sorted(hands.keys(), key=cmp_to_key(rank_hands))
    total_winnings = 0
    for rank, hand in enumerate(ranked_hands, 1):
        total_winnings += rank * hands[hand]
    print(total_winnings)


if __name__ == '__main__':
    main(read_input_from_file("07.txt"))
