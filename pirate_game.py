import time
from collections import defaultdict

def play_pirate_game(pirates, num_coins):
    num_pirates = len(pirates)
    final_distribution = {}
    
    while num_pirates > 0:
        captain = pirates[0]
        distribution = captain.propose_distribution(num_coins, num_pirates)
        print('\nVoting: ')
        print(f"{captain.name} proposes: {distribution}")
        
        if len(distribution) != num_pirates or sum(distribution) != num_coins:
            print(f"Invalid distribution proposed by {captain.name}")
            print(f"Expected {num_pirates} shares totaling {num_coins} coins")
            print(f"Got {len(distribution)} shares totaling {sum(distribution)} coins")
            pirates = pirates[1:]  # Remove the captain
            num_pirates -= 1
            # Update seniority of remaining pirates
            for i, pirate in enumerate(pirates):
                pirate.update_seniority(i)
            continue

        
        votes = [pirate.vote(distribution, num_coins, num_pirates) for pirate in pirates]
        
        print("Votes:", votes)

        # Count the number of True and False values
        true_count = votes.count(True)
        false_count = votes.count(False)
        
        # Get the total number of elements
        total_count = len(votes)
        
        # Calculate the percentages
        true_percentage = (true_count / total_count) * 100
        false_percentage = (false_count / total_count) * 100
        
        # Print the results
        print(f"Accept: {true_percentage:.0f}%")
        print(f"Reject: {false_percentage:.0f}%")
        print("")
        if sum(votes) >= num_pirates / 2:  # Majority or tie (captain has casting vote)
            print("✅ Distribution accepted! ")
            # Create final_distribution using pirate names as keys
            for i, pirate in enumerate(pirates):
                final_distribution[pirate.name] = distribution[i]
            break
        else:
            print(f"❌ {captain.name} walks the plank! 💀")
            final_distribution[captain.name] = 0
            pirates = pirates[1:]  # Remove the captain
            num_pirates -= 1
            # Update seniority of remaining pirates
            for i, pirate in enumerate(pirates):
                pirate.update_seniority(i)
    
    # If no distribution was accepted, the last pirate gets all coins
    if not final_distribution and num_pirates == 1:
        final_distribution[pirates[0].name] = num_coins
    
    # Pad the final distribution with zeros for pirates who walked the plank
    for pirate in pirates:
        if pirate.name not in final_distribution:
            final_distribution[pirate.name] = 0
    
    return final_distribution

def run_multiple_games(pirate_classes, num_coins):
    results = defaultdict(int)
    
    for i, pirate_class in enumerate(pirate_classes):
        print('\n######################################################################')

        print(f"--- GAME {i+1} ---")
        
        # Create new pirates for each game, with the specified pirate as captain
        pirates = [
            pirate_class(f"{pirate_class.__name__}", i)
            for i, pirate_class in enumerate(pirate_classes)
        ]
        
        # Rotate the list so the specified pirate is the captain (first in the list)
        pirates = pirates[i:] + pirates[:i]
        
        # Update seniority after rotation
        print('Rank:')
        for i, pirate in enumerate(pirates):
            pirate.update_seniority(i)
            # Create an instance of RationalPirate

            # Print the seniority of the RationalPirate
            if i == 0:
                print(f"   {pirate.seniority + 1}: {pirate.name} (Captain)")
            else:
                print(f"   {pirate.seniority + 1}: {pirate.name}")
        crew = ', '.join(n.__name__ for n in pirate_classes[1:])
        
        # Play the game
        distribution = play_pirate_game(pirates, num_coins)
        time.sleep(1)
        
        # Tally the results
        for pirate in pirates:
            results[pirate.__class__.__name__] += distribution[pirate.name]

        print(f"\nFinal distribution for this game:")
        for i, pirate in enumerate(distribution):
            print(f"   {i + 1}: {pirate} - {distribution[pirate]}")
    
    return results