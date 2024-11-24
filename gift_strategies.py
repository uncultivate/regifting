class Gifter:
    def __init__(self, name, seniority):
        self.name = name
        self.seniority = seniority
    
    def propose_distribution(self, num_gifts, num_gifters):
        raise NotImplementedError("Each gifter must implement their own distribution strategy")
    
    def vote(self, distribution, num_gifts, num_gifters):
        raise NotImplementedError("Each gifter must implement their own voting strategy")
    
class RationalGifter(Gifter):
    def propose_distribution(self, num_gifts, num_gifters):
        distribution = [0] * num_gifters
        remaining_gifts = num_gifts
        
        for i in range(num_gifters):
            if i == 0:  # The captain
                distribution[i] = remaining_gifts - (num_gifters // 2 - 1)
            elif i < num_gifters // 2:
                distribution[i] = 1
            remaining_gifts -= distribution[i]
        
        return distribution
    
    def vote(self, distribution, num_gifts, num_gifters):
        if not distribution or len(distribution) != num_gifters:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        my_share = distribution[self.seniority]
        expected_share = 1 if self.seniority < num_gifters // 2 else 0
        return my_share >= expected_share

class GreedyGifter(Gifter):
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

class EgalitarianGifter(Gifter):
    def propose_distribution(self, num_gifts, num_gifters):
        base_share = num_gifts // num_gifters
        distribution = [base_share] * num_gifters
        remainder = num_gifts % num_gifters
        for i in range(remainder):
            distribution[i] += 1
        return distribution
    
    def vote(self, distribution, num_gifts, num_gifters):
        if not distribution or len(distribution) != num_gifters:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        return max(distribution) - min(distribution) <= 1  # Accept if distribution is nearly equal

class RandomGifter(Gifter):
    import numpy as np

    def propose_distribution(self, num_gifts, num_gifters):
        distribution = [0] * num_gifters
        for gift in range(num_gifts):
            distribution[np.random.randint(num_gifters)] += 1
        return distribution
    
    def vote(self, distribution, num_gifts, num_gifters):
        if not distribution or len(distribution) != num_gifters:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        return np.random.random() < 0.5  # 50% chance of accepting any distribution

class VengefulGifter(Gifter):
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
        if self.seniority == 0:  # If captain, always vote yes
            return True
        return distribution[self.seniority] > distribution[0]  # Reject if captain gets more