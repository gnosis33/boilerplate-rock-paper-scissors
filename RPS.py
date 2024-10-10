def player(prev_play, opponent_history=[], my_history=[], strategy=['default'], count=[0]):
    import random

    # Update histories
    if prev_play:
        opponent_history.append(prev_play)
    if 'last_move' in locals():
        my_history.append(last_move)

    # Define the mappings
    beats = {'R': 'P', 'P': 'S', 'S': 'R'}
    loses_to = {'R': 'S', 'P': 'R', 'S': 'P'}

    # Detect if opponent is playing the move that beats our last move
    if len(opponent_history) > 1 and len(my_history) > 0:
        if opponent_history[-1] == beats[my_history[-1]]:
            count[0] += 1
        else:
            count[0] = 0  # Reset counter if pattern breaks

        # Increase threshold to 5 to reduce false positives
        if count[0] >= 5:
            strategy[0] = 'anti_kris'
        else:
            strategy[0] = 'default'

    # Strategy selection
    if strategy[0] == 'anti_kris':
        if len(my_history) > 0:
            next_move = loses_to[my_history[-1]]
        else:
            next_move = random.choice(['R', 'P', 'S'])
    else:
        # Increase n to 4 for better pattern recognition
        n = 4
        if len(opponent_history) < n:
            next_move = random.choice(['R', 'P', 'S'])
        else:
            # Build a frequency dictionary
            patterns = {}
            for i in range(len(opponent_history) - n):
                seq = ''.join(opponent_history[i:i + n])
                next_move_in_pattern = opponent_history[i + n]
                if seq not in patterns:
                    patterns[seq] = {'R': 0, 'P': 0, 'S': 0}
                patterns[seq][next_move_in_pattern] += 1

            last_seq = ''.join(opponent_history[-n:])
            if last_seq in patterns:
                # Predict the opponent's next move
                prediction = max(patterns[last_seq], key=patterns[last_seq].get)
                # Choose the move that beats the prediction
                next_move = beats[prediction]
            else:
                next_move = random.choice(['R', 'P', 'S'])

    last_move = next_move  # Save for the next round
    return next_move
