from mesa import Model
from FinancialAgent import FinancialAgent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
import numpy as np

class FinancialModel(Model):

    """A model with some number of agents."""

    def __init__(self, number_of_agents, width, height, strategy):

        # Set the number of agents.
        self.num_agents = number_of_agents

        # Create a MultiGrid of width x height cells.
        self.grid = MultiGrid(width, height, True)

        # Set the strategy.
        self.strategy = strategy

        # Create a schedule where agents will be activated randomly.
        self.schedule = RandomActivation(self)
        
        # Let the user know that if there are more agents than cells, the number of agents will be reduced.
        if self.num_agents > self.grid.width * self.grid.height:

            print("Number of agents is bigger than the number of cells. The number of agents will be reduced to " + str(self.grid.width * self.grid.height) + ".")

            self.num_agents = self.grid.width * self.grid.height

        # Create agents
        self.create_agents(self.num_agents)

        # Initialize data collectors. 
        self.initalize_data_collectors()

    def step(self):

        """Advance the model by one step."""

        self.schedule.step()

        self.collect_data()

    def create_agents(self, number_of_agents):
            
            # Create agents
            for i in range(self.num_agents):
    
                # Create agent object.
                a = FinancialAgent(i, self, 1, self.strategy, 1)
    
                # Add the agent to the schedule.
                self.schedule.add(a)
                
                # Add the agent to a random grid cell
                x = self.random.randrange(self.grid.width)
    
                y = self.random.randrange(self.grid.height)
                
                # If the cell is not empty, try again.
                while not self.grid.is_cell_empty((x, y)):
    
                    x = self.random.randrange(self.grid.width)
    
                    y = self.random.randrange(self.grid.height)
    
                # Place the agent in the cell.
                self.grid.place_agent(a, (x, y))
    
    def compute_gini(model):

        """Compute the Gini coefficient of the model."""

        # Get the wealth of each agent in the model.
        agent_wealths = [agent.wealth for agent in model.schedule.agents]

        # Sort the wealths.
        x = sorted(agent_wealths)

        # Find the number of agents.
        N = model.num_agents

        # Find the index of the median.
        B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))

        # Return the Gini coefficient.
        return (1 + (1 / N) - 2 * B)

    def get_wealthiest_agent(self):

        return max([agent.wealth for agent in self.schedule.agents])

    def compute_avg_wealth(self):

        return np.mean([agent.wealth for agent in self.schedule.agents])
    
    @staticmethod
    def current_wealthy_agents(model) -> int:
        
        return sum([1 for agent in model.schedule.agents if agent.wealth > 0])

    @staticmethod
    def current_non_wealthy_agents(model) -> int:

        return sum([1 for agent in model.schedule.agents if agent.wealth <= 0])


    def initalize_data_collectors(self):
    
        self.datacollector_gini = DataCollector(

            model_reporters={"Gini": self.compute_gini},
            agent_reporters={"Wealth": "wealth"}
        )
    
        self.datacollector_wealthiest_agent = DataCollector(

            model_reporters={"Wealthiest Agent": self.get_wealthiest_agent}
        )

        self.datacollector_currents = DataCollector(
            {
                "Wealthy Agents": self.current_wealthy_agents,
                "Non Wealthy Agents": self.current_non_wealthy_agents,
            }
        )

    def collect_data(self):

        self.datacollector_gini.collect(self)

        self.datacollector_wealthiest_agent.collect(self)

        self.datacollector_currents.collect(self)
