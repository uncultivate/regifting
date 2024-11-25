class Gifter:
    def __init__(self, name, seniority):
        self.name = name
        self.seniority = seniority
    
    def propose_distribution(self, num_gifts, num_gifters):
        raise NotImplementedError("Each gifter must implement their own distribution strategy")
    
    def vote(self, distribution, num_gifts, num_gifters):
        raise NotImplementedError("Each gifter must implement their own voting strategy")
    
    def update_seniority(self, new_seniority):
        self.seniority = new_seniority
    
class YourGifter(Gifter):
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
        pass

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
        pass

class GreedyGifter(Gifter): 
    # Takes almost everything, gives minimum to others
    def propose_distribution(self, num_gifts, num_gifters):
        distribution = [0] * num_gifters
        distribution[0] = num_gifts - (num_gifters - 1)  # Keep almost everything
        for i in range(1, num_gifters):
            distribution[i] = 1  # Give 1 gift to others
        return distribution
    
    def vote(self, distribution, num_gifts, num_gifters):
        if not distribution or len(distribution) != num_gifters:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        return distribution[self.seniority] > 0  # Accept any non-zero offer

class FairGifter(Gifter):
    # Distributes gifts equally
    def propose_distribution(self, num_gifts, num_gifters):
        base_share = num_gifts // num_gifters
        remainder = num_gifts % num_gifters
        distribution = [base_share] * num_gifters
        # Distribute remainder one by one
        for i in range(remainder):
            distribution[i] += 1
        return distribution
    
    def vote(self, distribution, num_gifts, num_gifters):
        if not distribution or len(distribution) != num_gifters:
            return False
        # Accept if distribution is relatively fair
        average = num_gifts / num_gifters
        return abs(distribution[self.seniority] - average) <= 1

class RandomGifter(Gifter):

    def propose_distribution(self, num_gifts, num_gifters):
        import numpy as np
        distribution = [0] * num_gifters
        for gift in range(num_gifts):
            distribution[np.random.randint(num_gifters)] += 1
        return distribution
    
    def vote(self, distribution, num_gifts, num_gifters):
        import numpy as np
        if not distribution or len(distribution) != num_gifters:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        return np.random.random() < 0.5  # 50% chance of accepting any distribution

