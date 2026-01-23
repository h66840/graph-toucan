from typing import Dict, List, Any, Optional
import random
from collections import Counter

def poker_win_calculator_analyse_poker_cards(my_cards_input: str, community_input: str, opponent_input: str) -> Dict[str, Any]:
    """
    Suggests poker actions based on the current game state by evaluating hand strength
    and simulating win probabilities using Monte Carlo method.

    Parameters:
    ----------
    my_cards_input : str
        The player's two cards as a space-separated string of rank+suit (e.g., 'As Kh')
    community_input : str
        The community cards as a space-separated string (e.g., 'Jd 10c 7h'), or empty if none
    opponent_input : str
        The opponent's cards as a space-separated string if known, or empty if unknown

    Returns:
    -------
    dict
        A dictionary containing:
        - 'win_probability': float, the calculated probability of winning the hand
        - 'suggested_action': str, the recommended action (fold, check/call, bet/raise)
        - 'best_hand': str or None, description of the best hand currently possible
    """
    # Validate inputs
    if not my_cards_input.strip():
        raise ValueError("Player's cards are required")
    
    # Parse cards
    def parse_card(card_str: str):
        if not card_str:
            return []
        return [c.strip().upper() for c in card_str.split() if c.strip()]
    
    my_cards = parse_card(my_cards_input)
    community_cards = parse_card(community_input)
    opponent_cards = parse_card(opponent_input)
    
    # Validate card counts
    if len(my_cards) != 2:
        raise ValueError("Player must have exactly 2 cards")
    
    if len(community_cards) > 5 or len(community_cards) < 0:
        raise ValueError("Community cards must be between 0 and 5")
    
    if opponent_cards and len(opponent_cards) != 2:
        raise ValueError("Opponent must have exactly 2 cards if provided")
    
    # Combine all known cards to check for duplicates
    all_known_cards = my_cards + community_cards + opponent_cards
    if len(all_known_cards) != len(set(all_known_cards)):
        raise ValueError("Duplicate cards detected")
    
    # Card utilities
    def card_rank(card: str) -> int:
        rank = card[:-1]
        if rank == 'J':
            return 11
        elif rank == 'Q':
            return 12
        elif rank == 'K':
            return 13
        elif rank == 'A':
            return 14
        else:
            return int(rank)
    
    def card_suit(card: str) -> str:
        return card[-1]
    
    # Evaluate best hand
    def evaluate_hand(cards):
        if len(cards) < 5:
            return None, "High Card"
        
        ranks = [card_rank(c) for c in cards]
        suits = [card_suit(c) for c in cards]
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        
        sorted_ranks = sorted(ranks, reverse=True)
        # Handle Ace-low straight
        if set(sorted_ranks) == {14, 5, 4, 3, 2}:
            is_ace_low_straight = True
            high_card = 5
        else:
            is_ace_low_straight = False
        
        # Check for flush
        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break
        
        # Check for straight
        unique_ranks = sorted(set(ranks), reverse=True)
        if is_ace_low_straight:
            straight_high = 5
        else:
            straight_high = None
            for i in range(len(unique_ranks) - 4):
                if all(unique_ranks[i] - j == unique_ranks[i + j] for j in range(5)):
                    straight_high = unique_ranks[i]
                    break
        
        # Check for straight flush
        if flush_suit:
            flush_cards = [r for r, s in zip(ranks, suits) if s == flush_suit]
            flush_ranks = sorted(set(flush_cards), reverse=True)
            if len(flush_ranks) >= 5:
                if set(flush_ranks) == {14, 5, 4, 3, 2}:
                    return 9, f"Straight Flush, Five High"
                for i in range(len(flush_ranks) - 4):
                    if all(flush_ranks[i] - j == flush_ranks[i + j] for j in range(5)):
                        high = flush_ranks[i]
                        if high == 14:
                            return 9, "Straight Flush, Ace High"
                        elif high == 13:
                            return 9, "Straight Flush, King High"
                        else:
                            return 9, f"Straight Flush, {high} High"
        
        # Four of a kind
        for rank, count in rank_counts.items():
            if count == 4:
                return 8, f"Four of a Kind, {rank_to_str(rank)}s"
        
        # Full house
        three_rank = None
        two_rank = None
        for rank, count in rank_counts.items():
            if count >= 3 and three_rank is None:
                three_rank = rank
            elif count >= 2:
                two_rank = rank
        if three_rank is not None and two_rank is not None:
            return 7, f"Full House, {rank_to_str(three_rank)}s over {rank_to_str(two_rank)}s"
        
        # Flush
        if flush_suit:
            flush_cards = [r for r, s in zip(ranks, suits) if s == flush_suit]
            high_card = max(flush_cards)
            return 6, f"Flush, {rank_to_str(high_card)} high"
        
        # Straight
        if straight_high is not None:
            return 5, f"Straight, {rank_to_str(straight_high)} high"
        if is_ace_low_straight:
            return 5, "Straight, Five high"
        
        # Three of a kind
        if three_rank is not None:
            return 4, f"Three of a Kind, {rank_to_str(three_rank)}s"
        
        # Two pair
        pairs = [rank for rank, count in rank_counts.items() if count >= 2]
        if len(pairs) >= 2:
            pairs = sorted(pairs, reverse=True)[:2]
            return 3, f"Two Pair, {rank_to_str(pairs[0])}s and {rank_to_str(pairs[1])}s"
        
        # One pair
        if len(pairs) == 1:
            return 2, f"Pair of {rank_to_str(pairs[0])}s"
        
        # High card
        return 1, f"High Card {rank_to_str(max(ranks))}"
    
    def rank_to_str(rank: int) -> str:
        if rank == 14:
            return "Ace"
        elif rank == 13:
            return "King"
        elif rank == 12:
            return "Queen"
        elif rank == 11:
            return "Jack"
        else:
            return str(rank)
    
    # Determine best hand
    all_player_cards = my_cards + community_cards
    best_hand = None
    if len(community_cards) > 0:
        best_hand = evaluate_hand(all_player_cards)[1]
    
    # Monte Carlo simulation for win probability
    def monte_carlo_simulation(my_cards, community_cards, opponent_cards, num_simulations=1000):
        # Build deck
        deck = []
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['h', 's', 'c', 'd']
        for r in ranks:
            for s in suits:
                card = r + s
                if card not in all_known_cards:
                    deck.append(card)
        
        wins = 0
        ties = 0
        
        for _ in range(num_simulations):
            # Shuffle deck
            sim_deck = deck.copy()
            random.shuffle(sim_deck)
            
            # Complete community cards
            remaining_community = sim_deck[:]
            final_community = community_cards.copy()
            while len(final_community) < 5:
                final_community.append(remaining_community.pop())
            
            # Opponent cards
            if opponent_cards:
                opp_cards = opponent_cards.copy()
            else:
                opp_cards = [remaining_community.pop(), remaining_community.pop()]
            
            # Evaluate hands
            my_final_hand = evaluate_hand(my_cards + final_community)
            opp_final_hand = evaluate_hand(opp_cards + final_community)
            
            if my_final_hand[0] > opp_final_hand[0]:
                wins += 1
            elif my_final_hand[0] == opp_final_hand[0]:
                # Compare high cards if same hand type
                my_ranks = sorted([card_rank(c) for c in my_cards + final_community], reverse=True)
                opp_ranks = sorted([card_rank(c) for c in opp_cards + final_community], reverse=True)
                
                for mr, or_ in zip(my_ranks, opp_ranks):
                    if mr > or_:
                        wins += 1
                        break
                    elif mr < or_:
                        break
                else:
                    ties += 1
        
        win_probability = (wins + ties * 0.5) / num_simulations
        return win_probability
    
    # Calculate win probability
    win_probability = 0.0
    if len(community_cards) == 0:
        # Pre-flop odds approximation
        win_probability = 0.5  # Simplified
    else:
        win_probability = monte_carlo_simulation(my_cards, community_cards, opponent_cards)
    
    # Suggest action based on win probability
    if win_probability > 0.75:
        suggested_action = "bet/raise"
    elif win_probability > 0.4:
        suggested_action = "check/call"
    else:
        suggested_action = "fold"
    
    return {
        "win_probability": win_probability,
        "suggested_action": suggested_action,
        "best_hand": best_hand
    }