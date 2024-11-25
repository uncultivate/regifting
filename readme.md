# 🎁 The Regifting Challenge

A Python implementation of a multiplayer gift distribution game where players propose and vote on how to distribute presents. The game explores different strategic approaches to resource allocation and voting behavior.

## 🎮 Game Rules

1. Each round has a director who proposes how to distribute a fixed number of presents among all players
2. All players (including the director) vote on the proposed distribution. The director holds the casting vote.
3. If majority accepts (≥50%), the distribution is implemented
4. If rejected, the director is eliminated (gets 0 presents) and the next player becomes director
5. Game continues until either:
   - A distribution is accepted
   - Only one player remains (who gets all presents)

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Required packages: `pandas`, `jupyter`

### Installation

```bash
git clone https://github.com/uncultivate/regifting
cd regifting
pip install -r requirements.txt
```

## 📝 Creating Your Own Gifter

The game's excitement comes from designing gifters with different strategies. Here's how to create your own gifter class:

### Basic Structure

Every gifter class must inherit from the base `Gifter` class and implement two methods:

```python
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
```

### Important Properties

Your gifter has access to:
- `self.name`: Your gifter's name (automatically assigned)
- `self.seniority`: Current position in the game (0 = director, updates each round)

### Example Strategies

1. **Greedy Gifter**: Takes almost everything, gives minimum to others
```python
class GreedyGifter(Gifter):
    def propose_distribution(self, num_gifts, num_gifters):
        distribution = [0] * num_gifters
        distribution[0] = num_gifts - (num_gifters - 1)  # Keep almost everything
        for i in range(1, num_gifters):
            distribution[i] = 1  # Give 1 gift to others
        return distribution
    
    def vote(self, distribution, num_gifts, num_gifters):
        if not distribution or len(distribution) != num_gifters:
            return False
        return distribution[self.seniority] > 0  # Accept any non-zero offer
```

2. **Fair Gifter**: Distributes gifts equally
```python
class FairGifter(Gifter):
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
```

### Strategy Tips

When designing your gifter, consider:

1. **As Director**:
   - How many gifts to keep vs distribute
   - Whether to favor certain positions
   - How to ensure majority approval

2. **As Voter**:
   - Minimum acceptable amount
   - Whether to form voting blocks
   - When to accept/reject strategic distributions

### Distribution Validation

Your distribution must:
- Have length equal to `num_gifters`
- Sum to exactly `num_gifts`
- Contain only non-negative integers

Invalid distributions result in elimination!

## 🎮 Running the Game

1. Open `run_game.ipynb` in Jupyter Notebook
2. Create your gifter classes. 
3. Initialize the game with your gifters:

```python
from game import GiftingGame

gifters = [YourGifter, GreedyGifter, FairGifter]  # Add your gifter classes
game = GiftingGame(gifter_classes=gifters, num_presents=100)
results = game.run_tournament()
```

The tournament will:
- Run multiple games
- Rotate starting positions
- Track total presents received
- Display results after each game

## 📊 Understanding Results

- Each gifter plays as director once
- Final scores show total presents accumulated
- Higher scores indicate more effective strategies

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingGifter`)
3. Commit your changes (`git commit -m 'Add AmazingGifter class'`)
4. Push to the branch (`git push origin feature/AmazingGifter`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 🙋‍♂️ Support

For questions or issues, please:
1. Check existing GitHub issues
2. Create a new issue with:
   - Your gifter class code
   - Expected behavior
   - Actual behavior
   - Full error message if applicable
