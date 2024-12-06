from collections import defaultdict
import random
import time
from typing import List, Dict, Type
import pandas as pd

class GiftingGame:
    """
    A class that manages the regifting game simulation where players propose and vote on gift distributions.
    
    The game follows these rules:
    1. Each round has a director who proposes a distribution of presents
    2. All players vote on the distribution
    3. If majority accepts, distribution is implemented
    4. If rejected, director is eliminated and gets 0 presents
    5. Game continues until a distribution is accepted or only one player remains
    """
    
    def __init__(self, gifter_classes: List[Type], num_presents: int):
        """
        Initialize the game with gifter classes and number of presents.
        
        Args:
            gifter_classes: List of gifter classes to participate in the game
            num_presents: Total number of presents to distribute
        """
        self.gifter_classes = gifter_classes
        self.num_presents = num_presents
        self.results = defaultdict(int)
        # Add statistics tracking
        self.stats = {
            'proposals': defaultdict(int),  # Track number of proposals per gifter
            'accepted_proposals': defaultdict(int),  # Track accepted proposals
            'self_gifts': defaultdict(int),  # Track gifts given to self
            'total_gifts_distributed': defaultdict(int),  # Track total gifts distributed
            'votes_cast': {'Accept': 0, 'Reject': 0},  # Track all votes
        }

    def _create_gifters(self, rotation: int) -> List:
        """
        Create and arrange gifters for a game round.
        
        Args:
            rotation: Number of positions to rotate the initial order
            
        Returns:
            List of initialized gifter objects in play order
        """
        # Create gifters with their initial positions and emojis
        original_order = [
            gifter_class(f"{gifter_class.__name__}", i)  # Default emoji if none specified
            for i, gifter_class in enumerate(self.gifter_classes)
        ]
        
        # Rotate order based on game number
        gifters = original_order[rotation:] + original_order[:rotation]
        
        # Randomize non-director positions
        return [gifters[0]] + random.sample(gifters[1:], len(gifters[1:]))

    def _validate_distribution(self, distribution: List[int], num_gifters: int) -> bool:
        """
        Validate if a proposed distribution is valid.
        
        Args:
            distribution: Proposed distribution of presents
            num_gifters: Current number of gifters
            
        Returns:
            bool: Whether distribution is valid
        """
        # Check if distribution has correct length
        if len(distribution) != num_gifters:
            return False
            
        # Calculate sum of distribution
        total = sum(distribution)
        
        # Allow for small floating point differences that can be rounded
        return abs(total - self.num_presents) < 1
        
    def _process_votes(self, gifters: List, distribution: List[int]) -> Dict:
        """Collect and process votes for a proposed distribution."""
        num_gifters = len(gifters)
        
        votes = ['Accept']  # Director's vote
        votes.extend(['Accept' if gifter.vote(distribution, self.num_presents, num_gifters) 
                     else 'Reject' for gifter in gifters[1:]])
        
        # Track individual votes (excluding director's vote)
        for gifter, vote in zip(gifters[1:], votes[1:]):
            self.stats[('votes', gifter.__class__.__name__, vote)] = \
                self.stats.get(('votes', gifter.__class__.__name__, vote), 0) + 1
        
        voting_tally = {gifter.name: vote for gifter, vote in zip(gifters, votes)}
        accept_count = votes.count('Accept')
        
        return {
            'tally': voting_tally,
            'accept_percentage': (accept_count / num_gifters) * 100,
            'reject_percentage': ((num_gifters - accept_count) / num_gifters) * 100,
            'is_accepted': accept_count >= num_gifters / 2
        }

    def play_single_game(self, gifters: List) -> Dict[str, int]:
        """
        Play a single game of regifting.
        
        Args:
            gifters: List of gifters participating in the game
            
        Returns:
            Dict mapping gifter names to their final present counts
        """
        num_gifters = len(gifters)
        final_distribution = {}
        
        # Update seniority of all gifters at the start
        for i, gifter in enumerate(gifters):
            gifter.update_seniority(i)
        
        while num_gifters > 0:
            director = gifters[0]
            distribution = director.propose_distribution(self.num_presents, num_gifters)
            
            # Track proposal statistics
            self.stats['proposals'][director.__class__.__name__] += 1
            
            # Display proposed distribution
            print(f"\nDirector {director.name} {director.emoji} proposes:")
            
            for i, (gifter, count) in enumerate(zip(gifters, distribution)):
                print(f"{i + 1}. {gifter.name} {gifter.emoji}: {count}")
            
            # Validate distribution
            if not self._validate_distribution(distribution, num_gifters):
                print(f"Invalid distribution from {director.name}")
                print(f"Expected {num_gifters} shares totaling {self.num_presents}")
                print(f"Got {len(distribution)} shares totaling {sum(distribution)}")
                gifters = gifters[1:]
                num_gifters -= 1
                continue
            
            # Process votes
            vote_results = self._process_votes(gifters, distribution)
            
            print("\nVotes:")
            for i, (name, vote) in enumerate(vote_results['tally'].items()):
                # Find the matching gifter to get their emoji
                gifter = next(g for g in gifters if g.name == name)
                print(f"{i + 1}. {name} {gifter.emoji}: {vote}")
            
            print("\nVote Tally:")
            print(f"Accept: {vote_results['accept_percentage']:.0f}%")
            print(f"Reject: {vote_results['reject_percentage']:.0f}%\n")
            
            if vote_results['is_accepted']:
                self.stats['accepted_proposals'][director.__class__.__name__] += 1
                # Track self-gifts and total gifts distributed
                self.stats['self_gifts'][director.__class__.__name__] += distribution[0]
                self.stats['total_gifts_distributed'][director.__class__.__name__] += sum(distribution)
                print("✅ Distribution accepted!")
                final_distribution.update({gifter.name: count for gifter, count in zip(gifters, distribution)})
                break
            else:
                print(f"Christmas is cancelled for {director.name} {director.emoji}!")
                print(f"{gifters[1].name} {gifters[1].emoji} is the new director!")
                final_distribution[director.name] = 0
                gifters = gifters[1:]
                num_gifters -= 1
            
            # Update seniority of remaining gifters
            for i, gifter in enumerate(gifters):
                gifter.update_seniority(i)
        
        # Handle last gifter or incomplete distribution
        if not final_distribution and num_gifters == 1:
            final_distribution[gifters[0].name] = self.num_presents
        
        # Fill in zeros for eliminated gifters
        for gifter in self.gifter_classes:
            gifter_name = gifter.__name__
            if gifter_name not in final_distribution:
                final_distribution[gifter_name] = 0
        
        return final_distribution

    def display_final_statistics(self):
        """Display comprehensive game statistics."""
        print("\n" + "="*50)
        print("🎉 FINAL GAME STATISTICS 🎉")
        print("="*50)
        
        # Proposal Success Rates
        print("\n📊 Proposal Success Rates:")
        for gifter in self.gifter_classes:
            name = gifter.__name__
            proposals = self.stats['proposals'][name]
            accepted = self.stats['accepted_proposals'][name]
            if proposals > 0:
                success_rate = (accepted / proposals) * 100
                print(f"{name}: {success_rate:.1f}% ({accepted}/{proposals} proposals accepted)")
        
        # Self-Gifting Behavior
        print("\n🎁 Self-Gifting Behavior:")
        for gifter in self.gifter_classes:
            name = gifter.__name__
            self_gifts = self.stats['self_gifts'][name]
            total_distributed = self.stats['total_gifts_distributed'][name]
            if total_distributed > 0:
                self_gift_rate = (self_gifts / total_distributed) * 100
                print(f"{name}: {self_gift_rate:.1f}% of distributed gifts kept for self")
        
        # Individual Voting Patterns
        print("\n🗳️ Individual Voting Patterns (non-director):")
        for gifter in self.gifter_classes:
            name = gifter.__name__
            accepts = self.stats.get(('votes', name, 'Accept'), 0)
            rejects = self.stats.get(('votes', name, 'Reject'), 0)
            total_votes = accepts + rejects
            if total_votes > 0:
                accept_rate = (accepts / total_votes) * 100
                reject_rate = (rejects / total_votes) * 100
                print(f"{name}: Accept {accept_rate:.1f}% | Reject {reject_rate:.1f}% ({total_votes} votes cast)")

    def run_tournament(self) -> Dict[str, int]:
        """
        Run a full tournament of games, rotating initial director position.
        
        Returns:
            Dict containing total presents received by each gifter type
        """
        num_games = len(self.gifter_classes)
        
        for game_num in range(num_games):
            print(f"""
                ╔══════════════════╗
                ║      GAME {game_num + 1:<4}   ║
                ╚══════════════════╝
                """)
            
            # Create and arrange gifters for this game
            gifters = self._create_gifters(game_num)
            
            # Play the game
            distribution = self.play_single_game(gifters)
            time.sleep(1)
            
            # Update running totals
            for gifter_name, presents in distribution.items():
                self.results[gifter_name.split()[0]] += presents
            
            # Display results
            print(f"\nFinal distribution for game {game_num + 1}:")
            for i, (gifter, presents) in enumerate(distribution.items(), 1):
                print(f"   {i}: {gifter} - {presents}")
            
            # Show running totals except after last game
            if game_num < num_games - 1:
                self._display_running_totals()
        
        # Add this at the end of the method, before returning
        self.display_final_statistics()
        
        return dict(self.results)

    def _display_running_totals(self):
        """Display current tournament standings in a formatted table."""
        df_results = pd.DataFrame(list(self.results.items()), 
                                columns=['Gifter Type', 'Total Presents'])
        df_results_sorted = (df_results.sort_values('Total Presents', ascending=False)
                            .reset_index(drop=True))
        df_results_sorted.index += 1
        print("\nRunning gifts tally:")
        print(df_results_sorted)