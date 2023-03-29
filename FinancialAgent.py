from mesa import Agent
import random
from Asset import Asset

class FinancialAgent(Agent):

    """An agent with fixed initial wealth."""

    def __init__(self, unique_id: int, model, wealth: int, strategy: str, mood: str):

        # Set the agent's unique_id and model.
        super().__init__(unique_id, model)

        # Set the agent's wealth.
        self.wealth = wealth

        # Set the agent's strategy.
        self.strategy = strategy

        # Set the agent's mood.
        self.mood = mood

        # Create an empty list for activities history
        self.history = []  

        # Define an empty list for the agent's assets.
        self.assets = []

        # Add gold to the agent's assets.
        self.assets.append(Asset("Gold", 1, 1))

        # Add silver to the agent's assets.
        self.assets.append(Asset("Silver", 0.5, 1))

        # Set the mean reversion threshold
        self.mean_reversion_threshold = 0.2

    def step(self):

        """A model step. Move, then trade with neighbors."""
        
        self.move()

        if self.wealth > 0:

            self.trade()            

        # Increase the price of gold and silver by 0.1 every 10 steps.
        if self.model.schedule.time % 10 == 0:
            
            for asset in self.assets:
    
                asset.price += 0.1

    
    def move(self):

        """Move the agent to a random empty cell."""

        # Get the position before moving.
        old_pos = self.pos

        # Get the neighborhood of the agent.
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        # Choose a random direction out of the possible steps.
        new_pos = self.random.choice(possible_steps)

        # Move the agent to the new position.
        self.model.grid.move_agent(self, new_pos)

        # Add the activity to the agent's history.
        self.history.append({'time': self.model.schedule.time,
                              'activity': 'move',
                              'old_pos': old_pos,
                              'new_pos': new_pos})

    def trade(self):

        """Trade with a random agent in the same cell."""

        # Get the agents in the same cell.
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        # If there is more than one agent in the cell, trade with one of them.
        if len(cellmates) > 1:
            
            # Choose a random agent to trade with.
            other = self.random.choice(cellmates)

            # Keep choosing until the other agent is not the same as the current agent
            while (other.unique_id == self.unique_id):

                other = self.random.choice(cellmates)

            if self.get_strategy() == "Asset Trading":
                    
                self.asset_trade(other)
            
            elif self.get_strategy() == "Wealth Trading":
                    
                self.wealth_trade(other)

            elif self.get_strategy() == "Mean Reversion":

                self.mean_reversion(other)
            
            elif self.get_strategy() == "Momentum":

                self.momentum_trade(other)

            # Add the activity to the agent's history.
            self.history.append({'time': self.model.schedule.time,
                                    'activity': 'trade',
                                    'other': other.unique_id,
                                    'wealth': self.wealth,
                                    'other_wealth': other.wealth})

    def asset_trade(self, other):

        # Check if the other agent has any assets.
        if len(other.assets) > 0:

            # Choose a random asset to trade.
            asset_to_trade = self.random.choice(other.assets)

            # Print the asset to trade.
            print("Agent " + str(self.unique_id) + " is interested in trading for " + str(asset_to_trade.get_name()) + " with Agent " + str(other.unique_id) + ".")

            # Get the price of the asset.
            asset_price = asset_to_trade.get_price()

            # If the agent has enough wealth to trade for the asset, trade.
            if self.wealth >= asset_price:
                    
                # Take the asset from the other agent.
                self.assets.append(asset_to_trade)

                # Remove the asset from the other agent.
                other.assets.remove(asset_to_trade)
        
                # Give the other agent the price of the asset.
                other.wealth += asset_price
        
                # Take the price of the asset from the agent.
                self.wealth -= asset_price

                # Print the trade.
                print("Agent " + str(self.unique_id) + " traded " + str(asset_to_trade.get_name()) + " with Agent " + str(other.unique_id) + " for " + str(asset_price) + " units of wealth.")

    def wealth_trade(self, other):
            
        # Check if the other agent has any wealth.
        if other.wealth > 0:
    
            # Choose a random amount of wealth to trade.
            wealth_to_trade = self.random.randint(1, self.wealth)
    
            # If the agent has enough wealth to trade, trade.
            if self.wealth >= wealth_to_trade:
                        
                # Give the other agent one wealth.
                other.wealth += wealth_to_trade
            
                # Take the wealth from the agent.
                self.wealth -= wealth_to_trade
    
                # Print the trade.
                print("Agent " + str(self.unique_id) + " traded " + str(wealth_to_trade) + " units of wealth with Agent " + str(other.unique_id) + ".")
    
    def mean_reversion(self, other):

        """ Implements mean reversion strategy. """
        
        # Check if the other agent has any assets.

        if len(other.assets) > 0: 
            
            # Choose a random asset to trade.
            asset_to_trade = self.random.choice(other.assets)

            # Print the asset to trade.
            print("Agent " + str(self.unique_id) + " is interested in trading for " + str(asset_to_trade.get_name()) + " with Agent " + str(other.unique_id) + ".")

            # Get the price of the asset.
            asset_price = asset_to_trade.get_price()

            print("Asset price: " + str(asset_price))

            # Calculate the mean price of the asset.
            mean_price = asset_to_trade.get_mean_price()

            print("Mean price: " + str(mean_price))

            # Calculate the difference between the asset price and the mean price.
            price_difference = asset_price - mean_price

            print("Price difference: " + str(price_difference))

            # Check if the difference is greater than the mean reversion threshold.
            if abs(price_difference) > self.mean_reversion_threshold:

                # Print the wealth of the agent.
                print("Agent " + str(self.unique_id) + " has " + str(self.wealth) + " units of wealth.")

                # Print what assets the other agent has.
                for asset in other.assets:

                    print("Agent " + str(other.unique_id) + " has " + str(asset.get_name()) + ".")


                if self.wealth >= asset_price and asset_to_trade in other.assets:

                        self.assets.append(asset_to_trade)

                        other.assets.remove(asset_to_trade)

                        other.wealth += asset_price

                        self.wealth -= asset_price

                        print("Agent " + str(self.unique_id) + " traded " + str(asset_to_trade.get_name()) + " with Agent " + str(other.unique_id) + " for " + str(asset_price) + " units of wealth.")
        
    def momentum_trade(self, other):
        pass

    def add_asset(self, asset):

        self.assets.append(asset)

    def get_assets(self):
            
        return self.assets

    def get_strategy(self):
    
        return self.strategy
    
    def get_mood(self):

        return self.mood

    def get_wealth(self):
    
        return self.wealth

    def get_history(self):
        
        return self.history 
    
    def get_unique_id(self):

        return self.unique_id

    def get_pos(self):

        return self.pos
    
    def get_color(self):

        return self.color
    
    def get_size(self):
            
        return self.size
    
    def get_label(self):

        return self.label

    def get_asset_names(self):
            
        asset_names = []
    
        for asset in self.assets:
    
            asset_names.append(asset.get_name())
    
        return asset_names
    
    def set_treshold(self, mean_reversion_threshold):

        self.mean_reversion_threshold = mean_reversion_threshold
    
    def get_threshold(self):

        return self.mean_reversion_threshold