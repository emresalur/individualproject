from mesa import Model
from agent import FinancialAgent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class FinancialModel(Model):
    """A model with some number of agents."""
    def __init__(self, number_of_agents, width, height, strategy):
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, True)
        self.strategy = strategy
        self.schedule = RandomActivation(self)
        self.running = True
        self.wealthiest_agent = 0

        # Create agents
        for i in range(self.num_agents):
            a = FinancialAgent(i, self, 1, 0.5)
            self.schedule.add(a)
            
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector_currents = DataCollector(
            {
                "Wealthy Agents": self.current_wealthy_agents,
                "Non Wealthy Agents": self.current_non_wealthy_agents,
            }
        )

        self.datacollector_gini  = DataCollector(
            model_reporters={"Gini": self.compute_gini},
            agent_reporters={"Wealth": "wealth"}
        )

        self.datacollector_transactions = DataCollector(
            model_reporters={"Transactions": self.transactions}
        )

        self.datacollector_wealthiest_agent = DataCollector(
            model_reporters={"Wealthiest Agent": self.get_wealthiest_agent}
        )


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector_currents.collect(self)
        self.datacollector_gini.collect(self)
        self.datacollector_transactions.collect(self)
        self.datacollector_wealthiest_agent.collect(self)
        
    def compute_gini(model):
        agent_wealths = [agent.wealth for agent in model.schedule.agents]
        x = sorted(agent_wealths)
        N = model.num_agents
        B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
        return (1 + (1 / N) - 2 * B)
    
    def get_wealthiest_agent(self):
        return max([agent.wealth for agent in self.schedule.agents])
            
    @staticmethod
    def current_wealthy_agents(model) -> int:
        return sum([1 for agent in model.schedule.agents if agent.wealth > 0])

    @staticmethod
    def current_non_wealthy_agents(model) -> int:
        return sum([1 for agent in model.schedule.agents if agent.wealth <= 0])
    
    def transactions(self):
        return sum([agent.transactions for agent in self.schedule.agents])