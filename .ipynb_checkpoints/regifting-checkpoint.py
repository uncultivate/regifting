import time
from collections import defaultdict
import random


def play_regifting(gifters, num_presents):
    num_gifters = len(gifters)
    final_distribution = {}
    
    while num_gifters > 0:
        director = gifters[0]
        distribution = director.propose_distribution(num_presents, num_gifters)
        print(f"\nDirector {director.name} is proposing this distribution of gifts:")
        proposed_distribution = {}
        for i, gifter in enumerate(gifters):
            proposed_distribution[gifter.name] = distribution[i]
        [print(f"{d[0]}: {d[1]}") for d in proposed_distribution.items()]
        
        if len(distribution) != num_gifters or sum(distribution) != num_presents:
            print(f"Invalid distribution proposed by {director.name}")
            print(f"Expected {num_gifters} shares totaling {num_presents} presents")
            print(f"Got {len(distribution)} shares totaling {sum(distribution)} presents")
            gifters = gifters[1:]  # Remove the director
            num_gifters -= 1
            # Update seniority of remaining gifters
            for i, gifter in enumerate(gifters):
                gifter.update_seniority(i)
            continue

        
        votes = [gifter.vote(distribution, num_presents, num_gifters) for gifter in gifters]
        
        # Convert to 'Accept' and 'Reject'
        votes = ['Accept' if x else 'Reject' for x in votes]
        
        print("\nVotes:")
        voting_tally = {}
        for i, gifter in enumerate(gifters):
            voting_tally[gifter.name] = votes[i]
        [print(f"{v[0]}: {v[1]}") for v in voting_tally.items()]

        # Count the number of True and False values
        true_count = votes.count('Accept')
        false_count = votes.count('Reject')
        
        # Get the total number of elements
        total_count = len(votes)
        
        # Calculate the percentages
        true_percentage = (true_count / total_count) * 100
        false_percentage = (false_count / total_count) * 100
        
        # Print the results
        print("\nVote Tally:")
        print(f"Accept: {true_percentage:.0f}%")
        print(f"Reject: {false_percentage:.0f}%")
        print("")
        if true_count >= num_gifters / 2:  # Majority or tie (director has casting vote)
            print("✅ Distribution accepted! ")
            # Create final_distribution using gifter names as keys
            for i, gifter in enumerate(gifters):
                final_distribution[gifter.name] = distribution[i]
            break
        else:
            print(f"❌ Christmas is cancelled for {director.name}! 😭")
            print(f"{gifters[1].name} is the new director!")
            final_distribution[director.name] = 0
            gifters = gifters[1:]  # Remove the director
            num_gifters -= 1
            # Update seniority of remaining gifters
            for i, gifter in enumerate(gifters):
                gifter.update_seniority(i)
    
    # If no distribution was accepted, the last gifter gets all presents
    if not final_distribution and num_gifters == 1:
        final_distribution[gifters[0].name] = num_presents
    
    # Pad the final distribution with zeros for gifters whose Christmases were cancelled
    for gifter in gifters:
        if gifter.name not in final_distribution:
            final_distribution[gifter.name] = 0
    
    return final_distribution

import random

def run_multiple_games(gifter_classes, num_presents):
    results = defaultdict(int)
    
    # Preserve the original order of gifters
    original_order = [
        gifter_class(f"{gifter_class.__name__}", i)
        for i, gifter_class in enumerate(gifter_classes)
    ]
    
    num_games = len(gifter_classes)
    
    for i in range(num_games):
        print('\n######################################################################')
        print(f"\n--- GAME {i+1} ---")
        
        # Rotate the order of directors
        gifters = original_order[i:] + original_order[:i]
        
        # Shuffle non-directors
        non_directors = gifters[1:]
        random.shuffle(non_directors)
        gifters = [gifters[0]] + non_directors  # Ensure the director stays first
        
        # Play the game
        distribution = play_regifting(gifters, num_presents)
        time.sleep(1)
        
        # Tally results
        for gifter in gifters:
            results[gifter.__class__.__name__] += distribution[gifter.name]

        print(f"\nFinal distribution for this game:")
        for k, gifter in enumerate(distribution):
            print(f"   {k + 1}: {gifter} - {distribution[gifter]}")

        # Display running totals
        df_results = pd.DataFrame(list(results.items()), columns=['Gifter Type', 'Total Presents'])
        df_results_sorted = df_results.sort_values('Total Presents', ascending=False).reset_index(drop=True)
        df_results_sorted.index = df_results_sorted.index + 1
        if i < num_games - 1:
            print("\nRunning gifts tally:")
            print(df_results_sorted)
    
    return results