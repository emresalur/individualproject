from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import FinancialModel
from mesa.visualization.modules import ChartModule

NUMBER_OF_CELLS = 100

SIZE_OF_CANVAS_IN_PIXELS_X = 800
SIZE_OF_CANVAS_IN_PIXELS_Y = 800

simulation_params = {
    "number_of_agents": UserSettableParameter(
        "slider", 
        "Number of agents", 
        100, # default
        10, # min
        200, # max
        1, # step
        description="Choose how many agents to include in the simulation.",
    ),

    "strategy": UserSettableParameter(
        "choice",
        "Trading Strategy",
        value="Random", # default
        choices=["Random", "Greedy", "Risk Averse", "Barter", "Gift"],
        description="Choose the trading strategy for the agents.",
    ),

    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
}

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    
    if agent.wealth > 0:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal

grid = CanvasGrid(agent_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)

chart_currents = ChartModule(
    [
        {"Label": "Wealthy Agents", "Color": "Green"},
        {"Label": "Non Wealthy Agents", "Color": "Red"},
    ],
    canvas_height=300,
    data_collector_name="datacollector_currents"
)

gini = ChartModule(
    [
        {"Label": "Gini", "Color": "Blue"},
    ],
    data_collector_name="datacollector_gini"
)

transactions = ChartModule(
    [
        {"Label": "Transactions", "Color": "Black"},
    ],
    data_collector_name="datacollector_transactions"
)

wealthiest_agent = ChartModule(
    [
        {"Label": "Wealthiest Agent", "Color": "Purple"},
    ],
    data_collector_name="datacollector_wealthiest_agent"
)

server = ModularServer(FinancialModel, [grid, chart_currents, gini, transactions, wealthiest_agent], "Money Model", simulation_params)
server.port = 8521 # The default
server.launch()