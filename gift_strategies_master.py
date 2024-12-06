class Gifter:
    def __init__(self, name, emoji, seniority):
        self.name = name
        self.emoji = emoji
        self.seniority = seniority
    
    def propose_distribution(self, num_gifts, num_gifters):
        raise NotImplementedError("Each gifter must implement their own distribution strategy")
    
    def vote(self, distribution, num_gifts, num_gifters):
        raise NotImplementedError("Each gifter must implement their own voting strategy")
    
    def update_seniority(self, new_seniority):
        self.seniority = new_seniority
    
class TheGrinch(Gifter):
    def __init__(self, name, seniority):
        super().__init__(name, "🤢", seniority)  # Brain

    def propose_distribution(self, num_gifts, num_gifters):
        distribution = [0] * num_gifters
        
        if num_gifters <= 2:
            for i in range(num_gifters):
                if i == 0:  # The director
                    distribution[i] = num_gifts
                else:
                    distribution[i] = 0
        else:
            if num_gifts > 2:
                # Give nothing to the assistant director, they want your job
                distribution[1] = 0
                
                # Give a measly 1 gift to everyone else
                for i in range(2, num_gifters):
                    distribution[i] = 1
                
                # The remainder goes to the director
                distribution[0] = num_gifts - (num_gifters - 2)
            else:
                # Original logic for 2 or fewer gifts
                for i in range(num_gifters):
                    if i == 0:  # The director
                        distribution[i] = num_gifts - (num_gifters // 2 - 1)
                    elif i < num_gifters // 2:
                        distribution[i] = 1
            
        return distribution
    
    def vote(self, distribution, num_gifts, num_gifters):
        # If this is the first seniority level, always return False
        if self.seniority == 1:
            return False
        # Accept any non-zero share for all other seniority levels
        return distribution[self.seniority] > 0

class GimmeGimmeGimme(Gifter):
    def __init__(self, name, seniority):
        super().__init__(name, "🤑", seniority)  # Party
    def propose_distribution(self, num_gifts: int, num_gifters: int) -> list:
        """Propose I get all presents, on the off-chance it gets accepted!"""
        distribution = [0] * num_gifters
        distribution[0] = num_gifts
        return distribution

    def vote(self, distribution: list, num_gifts: int, num_gifters: int) -> bool:
        """Accept only if I get it all!"""
        if self.seniority == 0:
            return True
        elif distribution[self.seniority] == num_gifts:
            return True
        else:
            return False

class NoGift4U(Gifter):
    def __init__(self, name, seniority):
        super().__init__(name, "🍲", seniority)  # Party
    # Based on pirate strategy - only allocate gifts to every second gifter. But more generous - allocate base share to each
    def propose_distribution(self, num_gifts, num_gifters):
        base_share = num_gifts // num_gifters
        distribution = [0] * num_gifters
        # Allocate to every second person the base share. 0 for others.
        for i in range(2,num_gifters,2):
            distribution[i] += base_share
        # Allocate all remaining gifts to self.    
        distribution[0] = num_gifts - sum(distribution)
        return distribution
    
    def vote(self, distribution, num_gifts, num_gifters):
        if not distribution or len(distribution) != num_gifters:
            return False
        return distribution[self.seniority] > 0 and self.seniority != 1  # Accept any non-zero offer when not next in line of seniority

class RevelrousRyan(Gifter):
    def __init__(self, name, seniority):
        super().__init__(name, "🥺", seniority)  # Party

    def propose_distribution(self, num_gifts: int, num_gifters: int) -> list:
        """
        Create a proposed distribution of gifts. To be used when YOU are the director.

        Args:
            num_gifts: Total number of gifts to distribute
            num_gifters: Number of players still in the game

        Returns:
            list: Proposed distribution where index represents player position 
                 (0 is self, 1 is next player, etc.)
        """
        per_person_gift = int(num_gifts/num_gifters)
        return [num_gifts - (per_person_gift * (num_gifters - 1))] + [per_person_gift] * (num_gifters - 1)

    def vote(self, distribution: list, num_gifts: int, num_gifters: int) -> bool:
        """
        Vote on a proposed distribution.

        Args:
            distribution: Proposed distribution of gifts
            num_gifts: Total number of gifts
            num_gifters: Number of players still in game

        Returns:
            bool: True to accept, False to reject
        """
        return False

class QuackQuackQuack(Gifter):
    def __init__(self, name, seniority):
        super().__init__(name, "🦆", seniority)  # Duck

    def integer_root(self, n):
        i = 0
        while (i ** 2 < n):
            i += 1
        return i
    def propose_distribution(self, num_gifts: int, num_gifters: int) -> list:
        needed = num_gifters / 2
        needed = needed + needed % 1 - 1
        margin = self.integer_root(needed)
        needed = int(needed + margin)
        if needed > num_gifters - 1:
            needed = num_gifters - 1
        a = num_gifts / num_gifters + 0.00001
        res = [0] * num_gifters
        for i in range(needed):
            res[num_gifters - 1 - i] = a
        res[0] = num_gifts - a * needed
        return res

    def vote(self, distribution: list, num_gifts: int, num_gifters: int) -> bool:
        if self.seniority == 0:
            return True
        elif num_gifters == 3 and self.seniority == 1:
            return False
        else:
            reject_expectation = num_gifts / (num_gifters - 1)
            return distribution[self.seniority] >= reject_expectation

class MrGauss(Gifter):
    def __init__(self, name, seniority):
        super().__init__(name, "🧐", seniority)  # Chart

    def propose_distribution(self, num_gifts: int, num_gifters: int) -> list:
        """
        Create a gaussian distribution for all presents
        """
        import numpy as np
        import scipy.stats as stats

        x = np.linspace(0, num_gifters, num_gifters)
        
        distr = [0]*num_gifters
        for i in range(num_gifts):
            index = np.clip(
                int(np.random.normal(num_gifters/2, num_gifters/5)),
                # int(np.random.uniform(0, num_gifters)),
                0,
                num_gifters-1
            )
            distr[index] += 1
        return distr

    def vote(self, distribution: list, num_gifts: int, num_gifters: int) -> bool:
        """
        If the distribution looks gaussian enough - accept.
        """
        import scipy.stats as stats

        if num_gifters > 2:
            # Check if all values are the same
            if len(set(distribution)) == 1:
                return False  # Reject completely uniform distributions
            
            test = stats.shapiro(distribution)[1]
            return test > 0.05
        else:
            test = abs(distribution[0] - distribution[1])
            return test < 5

class Harpo(Gifter):
    def __init__(self, name, seniority):
        super().__init__(name, "🤗", seniority)  # Chart
    def propose_distribution(self, num_gifts, num_gifters):
        """
        'You get a gift! And you get a gift! Everybody gets a gift!'
                --Oprah
        Gifts are allocated with an Oprah-approved weighted curve, ensuring 
        the higher ranks feel special while the rest aren't left empty-handed. 
        Of course, I keep 50% of the gifts for myself (Oprah keeps her luxury too). 
        Any remaining gifts are distributed randomly, because life (and Oprah) 
        loves surprises.
        """
        distribution = [0] * num_gifters

        # Allocate a specified number of gifts to a specific player
        def you_get_a_gift(player_index, num_given):
            """
            Allocates a specified number of gifts to the specified player.

            Args:
                player_index: Index of the player receiving the gifts.
                num_given: Number of gifts to allocate.
            """
            distribution[player_index] += num_given

        # Randomly allocate a specified number of gifts
        def look_under_your_chair(num_remaining):
            """
            Allocates a specified number of gifts randomly to players.

            Args:
                num_remaining: Number of gifts to allocate.
            """
            import random
            for _ in range(num_remaining):
                random_index = random.randint(0, num_gifters - 1)
                you_get_a_gift(random_index, 1)

        # Keep 50% of the gifts
        self_share = num_gifts // 2
        you_get_a_gift(0, self_share)
        num_gifts -= self_share

        # Generate a weighted gift curve for the remaining players
        weights = [1 / (i + 1) for i in range(1, num_gifters)]  # Exponential decay
        total_weight = sum(weights)

        # Distribute gifts proportionally to weights
        for rank, weight in enumerate(weights, start=1):
            share = int((weight / total_weight) * num_gifts)  # Proportional share
            you_get_a_gift(rank, share)
            num_gifts -= share

        # Allocate any leftover gifts randomly
        look_under_your_chair(num_gifts)

        return distribution

    def vote(self, distribution, num_gifts, num_gifters):
        """
        Vote based on rank-weighted fairness: reject if share is less than rank-based fair share
        or if lower-ranked players get more.
        """
        my_share = distribution[self.seniority]
        director_share = distribution[0]

        # Calculate rank-based fair share
        rank_weight = num_gifters - self.seniority
        total_weight = num_gifters * (num_gifters + 1) // 2
        fair_share = (rank_weight / total_weight) * num_gifts

        # Reject if share is below rank-weighted fair share
        if my_share < fair_share:
            return False

        # Reject if the director keeps more than half the gifts
        if director_share > num_gifts / 2:
            return False

        # Reject if any lower-ranked player gets more
        for i in range(self.seniority + 1, num_gifters):
            if distribution[i] > my_share:
                return False

        # Accept if none of the rejection criteria are met
        return my_share > 0

class M_gifter(Gifter):
    def __init__(self, name, seniority):
        super().__init__(name, "🌻", seniority)  # Chart
    def propose_distribution(self, num_gifts, num_gifters):
        # Share the gifts with 70% of the people hoping they vote yes. I also get the remainder. 
        included_count = max(1, int(num_gifters * 0.7))  # At least 1 player included

        # Ensure that the number of people im gifting too doesn't exceed the total number of players
        included_count = min(included_count, num_gifters)

        # Initialize distribution
        distribution = [0] * num_gifters

        # Distribute gifts equally among the included players
        share_per_person = num_gifts // included_count
        for i in range(included_count):
            distribution[i] = share_per_person

        # Distribute any remainder to me
        remainder = num_gifts - sum(distribution)
        distribution[0] += remainder

        return distribution

    
    def vote(self, distribution, num_gifts, num_gifters):
    # being grateful for any number of gifts
        if distribution[self.seniority] > 0:
            return True
        else:
            return False


