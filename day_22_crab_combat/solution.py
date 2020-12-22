from collections import deque


# File parsing #


def parse_file(file_name):
    with open(file_name) as f:
        data = f.read().split('\n\n')
    data[1] = data[1][:-1]
    return [deque([int(x) for x in d.split('\n')[1:]]) for d in data]


# Standard Combat (AKA War) #


game_number = 0
round_numbers = [0]


def get_winner(deck1, deck2):
    if len(deck2) == 0:
        print(f"Player 1 wins game {game_number}!")
        return deck1, 1
    if len(deck1) == 0:
        print(f"Player 2 wins game {game_number}!")
        return deck2, 2
    return None, None


def do_combat_round(deck1, deck2):
    p1_card = deck1.popleft()
    p2_card = deck2.popleft()
    if p1_card > p2_card:
        print(f"Player 1 wins round {round_numbers[game_number - 1]} of game {game_number}!\n")
        deck1.extend((p1_card, p2_card))
    else:
        print(f"Player 2 wins round {round_numbers[game_number - 1]} of game {game_number}!\n")
        deck2.extend((p2_card, p1_card))
    return get_winner(deck1, deck2)


def combat(deck1, deck2, is_recursive=False):
    global game_number, round_numbers

    if is_recursive:
        return recursive_combat(deck1, deck2)

    game_number = 1
    round_numbers[0] = 0

    winning_deck = None
    winner = None
    while winning_deck is None:
        round_numbers[0] += 1
        print(f"-- Round {round_numbers[0]} --")
        print(f"P1's Deck: {deck1}")
        print(f"P2's Deck: {deck2}")
        winning_deck, winner = do_combat_round(deck1, deck2)
    score = score_deck(winning_deck)
    return winner, score


# Recursive Combat #


def copy_deck_for_recurse(num_cards, deck):
    sub_game_deck = deque()
    items = []
    for i in range(num_cards):
        next_item = deck.popleft()
        items.append(next_item)
        sub_game_deck.append(next_item)
    deck.extendleft(items[::-1])
    return sub_game_deck


def do_recursive_combat_round(deck1, deck2):
    if deck1[0] >= len(deck1) or deck2[0] >= len(deck2):
        return do_combat_round(deck1, deck2)  # Not enough cards for recursion; this round runs normally.
    else:
        print(f"Entering game {game_number + 1} to determine round winner...")
        p1_card = deck1.popleft()
        p2_card = deck2.popleft()
        sub_game_deck1 = copy_deck_for_recurse(p1_card, deck1)
        sub_game_deck2 = copy_deck_for_recurse(p2_card, deck2)
        winner, _ = recursive_combat(sub_game_deck1, sub_game_deck2)
        if winner == 1:
            print(f"Player 1 wins round {round_numbers[game_number - 1]} of game {game_number}!\n")
            deck1.extend((p1_card, p2_card))
        else:
            print(f"Player 2 wins round {round_numbers[game_number - 1]} of game {game_number}!\n")
            deck2.extend((p2_card, p1_card))
        return get_winner(deck1, deck2)


def recursive_combat(deck1, deck2):
    global game_number, round_numbers

    winning_deck = None
    winner = None
    state_histories = {}
    game_number += 1
    print(f"\n=== Game {game_number} ===\n")
    if len(round_numbers) < game_number:
        round_numbers.append(0)
    else:
        round_numbers[game_number - 1] = 0
    while winning_deck is None:
        round_numbers[game_number - 1] += 1
        print(f"-- Round {round_numbers[game_number - 1]} --")
        print(f"P1's Deck: {deck1}")
        print(f"P2's Deck: {deck2}")

        state_histories[repr(deck1) + repr(deck2)] = True
        winning_deck, winner = do_recursive_combat_round(deck1, deck2)
        if repr(deck1) + repr(deck2) in state_histories:
            # These two things occur simultaneously:
            # 1. This condition evaluates to True
            # 2. The watch on this condition evaluates to False
            # I'm sure there's a *perfectly rational* explanation for that.
            print(f"Player 1 wins game {game_number} due to infinite recursion prevention rule!")
            game_number -= 1
            if game_number > 0:
                print(f"Back to game {game_number}...")
            return 1, score_deck(deck1)
    score = score_deck(winning_deck)
    game_number -= 1
    if game_number > 0:
        print(f"\nBack to game {game_number}...")
    return winner, score


# Scoring #


def score_deck(deck):
    score = 0
    multiplier = 0
    for i in range(len(deck)):
        multiplier += 1
        score += deck.pop() * multiplier
    return score


if __name__ == '__main__':
    for recursive in [False, True]:
        decks = parse_file('input.txt')
        game_winner, winning_score = combat(decks[0], decks[1], recursive)
        print(f"Player {game_winner} wins at{' Recursive' if recursive else ''} Combat. Score: {winning_score}")
