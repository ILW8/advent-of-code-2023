from functools import cmp_to_key
from typing import List
from input_reader import read_input_from_file
from collections import Counter

CARD_VALUE = {k: v for v, k in enumerate("23456789TJQKA")}
CARD_VALUE_PART2 = {k: v for v, k in enumerate("J23456789TQKA")}
JOKER_POTENTIALS = "23456789TQKA"


def find_strongest_hand(hand):
    """
    Find a new hand where Js are replaced with any other card such that the new hand becomes the strongest type of hand
    possible. tiebreaker_joker can be used with the result of this for complete comparison between two hands.
    """
    if hand == "JJJJJ":
        return hand

    card_counts = Counter(hand)
    del card_counts["J"]
    max_card, max_count = card_counts.most_common(1)[0]
    new_hand = [card if card != "J" else max_card for card in hand]  # Replace Js with the next highest occurrence card

    return new_hand


def tiebreaker_joker(left: str, right: str):
    for card_idx in range(5):
        if CARD_VALUE_PART2[left[card_idx]] < CARD_VALUE_PART2[right[card_idx]]:
            return -1
        if CARD_VALUE_PART2[left[card_idx]] > CARD_VALUE_PART2[right[card_idx]]:
            return 1
    return 0


def rank_hands_part2(left: str, right: str):
    cards_count_left = Counter(left)
    cards_count_right = Counter(right)

    max_left = max(cards_count_left.values())
    max_right = max(cards_count_right.values())

    if max_left < max_right:
        return -3
    if max_left > max_right:
        return 3

    # possibilities left: 1) full house vs three of a kind   2) two pair vs 1 pair  3) same kind

    # handle 1) and 2)
    if max_left in (2, 3):
        if -len(cards_count_left) < -len(cards_count_right):
            return -2
        if -len(cards_count_left) > -len(cards_count_right):
            return 2

    # handle 3) same kind -> let tiebreaker_joker handle it
    return 0


def rank_hands_part2_entrypoint(left: str, right: str):
    new_left = find_strongest_hand(left)
    new_right = find_strongest_hand(right)

    retval = rank_hands_part2(new_left, new_right)
    if retval != 0:
        return retval

    return tiebreaker_joker(left, right)


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
    print(f"{total_winnings=}")


def part2(input_lines: List[str]):
    hands = {}
    new_hands = {}
    for line in input_lines:
        hand = line.split()[0]
        bid = int(line.split()[1])
        hands[hand] = bid
        new_hands[hand] = find_strongest_hand(hand)

    ranked_hands = sorted(hands.keys(), key=cmp_to_key(rank_hands_part2_entrypoint))
    # print("---")
    # for r in ranked_hands:
    #     print(f"{r} ({new_hands[r]}) {', '.join(map(str, sorted(Counter(new_hands[r]).values(), reverse=True)))}")
    # print('---')
    total_winnings_part2 = 0
    for rank, hand in enumerate(ranked_hands, 1):
        total_winnings_part2 += rank * hands[hand]
    print(f"{total_winnings_part2=}")


if __name__ == '__main__':
    main(read_input_from_file("07.txt"))
    part2(read_input_from_file("07.txt"))
