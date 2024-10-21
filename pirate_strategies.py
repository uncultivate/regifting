import numpy as np

class Pirate:
    def __init__(self, name, seniority):
        self.name = name
        self.seniority = seniority
    
    def propose_distribution(self, num_coins, num_pirates):
        raise NotImplementedError("Each pirate must implement their own distribution strategy")
    
    def vote(self, distribution, num_coins, num_pirates):
        raise NotImplementedError("Each pirate must implement their own voting strategy")
    
    def update_seniority(self, new_seniority):
        self.seniority = new_seniority

class RationalPirate(Pirate):
    def propose_distribution(self, num_coins, num_pirates):
        distribution = [0] * num_pirates
        remaining_coins = num_coins
        
        for i in range(num_pirates):
            if i == 0:  # The captain
                distribution[i] = remaining_coins - (num_pirates // 2 - 1)
            elif i < num_pirates // 2:
                distribution[i] = 1
            remaining_coins -= distribution[i]
        
        return distribution
    
    def vote(self, distribution, num_coins, num_pirates):
        if not distribution or len(distribution) != num_pirates:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        my_share = distribution[self.seniority]
        expected_share = 1 if self.seniority < num_pirates // 2 else 0
        return my_share >= expected_share

class GreedyPirate(Pirate):
    def propose_distribution(self, num_coins, num_pirates):
        distribution = [0] * num_pirates
        distribution[0] = num_coins - (num_pirates - 1)  # Keep almost everything
        for i in range(1, num_pirates):
            distribution[i] = 1  # Give 1 coin to others
        return distribution
    
    def vote(self, distribution, num_coins, num_pirates):
        if not distribution or len(distribution) != num_pirates:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        return distribution[self.seniority] > 0  # Accept any non-zero offer

class EgalitarianPirate(Pirate):
    def propose_distribution(self, num_coins, num_pirates):
        base_share = num_coins // num_pirates
        distribution = [base_share] * num_pirates
        remainder = num_coins % num_pirates
        for i in range(remainder):
            distribution[i] += 1
        return distribution
    
    def vote(self, distribution, num_coins, num_pirates):
        if not distribution or len(distribution) != num_pirates:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        return max(distribution) - min(distribution) <= 1  # Accept if distribution is nearly equal

class RandomPirate(Pirate):
    def propose_distribution(self, num_coins, num_pirates):
        distribution = [0] * num_pirates
        for coin in range(num_coins):
            distribution[np.random.randint(num_pirates)] += 1
        return distribution
    
    def vote(self, distribution, num_coins, num_pirates):
        if not distribution or len(distribution) != num_pirates:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        return np.random.random() < 0.5  # 50% chance of accepting any distribution

class VengefulPirate(Pirate):
    def propose_distribution(self, num_coins, num_pirates):
        distribution = [0] * num_pirates
        distribution[0] = num_coins - (num_pirates - 1)  # Keep almost everything
        for i in range(1, num_pirates):
            distribution[i] = 1  # Give 1 coin to others
        return distribution
    
    def vote(self, distribution, num_coins, num_pirates):
        if not distribution or len(distribution) != num_pirates:
            print(f"{self.name}: Invalid distribution, voting No")
            return False
        if self.seniority == 0:  # If captain, always vote yes
            return True
        return distribution[self.seniority] > distribution[0]  # Reject if captain gets more