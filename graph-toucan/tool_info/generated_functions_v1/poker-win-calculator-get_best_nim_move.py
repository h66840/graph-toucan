from typing import Dict, List, Any, Optional
import ast

def poker_win_calculator_get_best_nim_move(piles: str) -> Dict[str, Any]:
    """
    Determine the best move in a Nim game using the nim-sum strategy.
    
    Args:
        piles (str): A string representation of a list of integers representing the number of objects in each pile.
        
    Returns:
        A dictionary containing:
        - pile_index (int): index of the pile from which to remove objects in the best move
        - objects_to_remove (int): number of objects to remove from the specified pile in the best move
        - error (str, optional): error message if the tool execution failed, otherwise absent
    """
    try:
        # Parse the input string into a list of integers using safe evaluation
        pile_list = ast.literal_eval(piles)
        if not isinstance(pile_list, list):
            return {"error": "Input must be a list of integers."}
        if not all(isinstance(x, int) and x >= 0 for x in pile_list):
            return {"error": "All pile values must be non-negative integers."}
        if len(pile_list) == 0:
            return {"error": "Pile list cannot be empty."}

        # Compute the nim-sum (XOR of all pile sizes)
        nim_sum = 0
        for pile in pile_list:
            nim_sum ^= pile

        # If nim-sum is 0, no winning move exists; make a safe move (reduce first non-empty pile by 1)
        if nim_sum == 0:
            for i, pile in enumerate(pile_list):
                if pile > 0:
                    return {"pile_index": i, "objects_to_remove": 1}
            # If all piles are zero, return no move
            return {"pile_index": 0, "objects_to_remove": 0}

        # Find a move that makes the nim-sum zero
        for i, pile in enumerate(pile_list):
            target = pile ^ nim_sum
            if target < pile:
                return {"pile_index": i, "objects_to_remove": pile - target}

        # Fallback: should not reach here if logic is correct
        return {"pile_index": 0, "objects_to_remove": 1}

    except (ValueError, SyntaxError) as e:
        return {"error": f"Failed to parse input: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to compute best move: {str(e)}"}