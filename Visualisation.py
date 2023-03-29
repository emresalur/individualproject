from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.modules import BarChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter
from FinancialModel import FinancialModel

class CustomCSS(VisualizationElement):
    package_includes = ["my_style.css"]
    local_includes = ["my_style.css"]

NUMBER_OF_CELLS = 10

SIZE_OF_CANVAS_IN_PIXELS_X = 500

SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {
    "number_of_agents": UserSettableParameter(
        "slider", 
        "Number of agents", 
        10, # default
        1, # min
        20, # max
        1, # step
        description="Choose how many agents to include in the simulation.",
    ),

    "strategy": UserSettableParameter(
        "choice",
        "Trading Strategy",
        value="Asset Trading", # default
        choices=["Asset Trading", "Wealth Trading", "Mean Reversion", "Momentum"],
        description="Choose the trading strategy for the agents.",
    ),

    "width": NUMBER_OF_CELLS,

    "height": NUMBER_OF_CELLS,
}

def wealth_to_radius(wealth):

    """Maps the agent's wealth to a radius size."""
    return 0.25 + wealth * 0.1  # add 0.1 to make sure the minimum radius is 0.5

def agent_portrayal(agent):
    """Returns the portrayal of the given agent."""

    radius = wealth_to_radius(agent.wealth)

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": radius,
        "Layer": 0 if agent.wealth > 0 else 1,
        "Color": "green",
        "text": agent.unique_id,
        "text_color": "black",
    }

    #Determine the agent's color based on its wealth
    if agent.wealth > 0:

        # Highlight the wealthiest agent after 10 steps
        if agent.wealth == agent.model.get_wealthiest_agent() and agent.model.schedule.time > 10:

            portrayal["Color"] = "gold"
            portrayal["Layer"] = 2
        else:

            portrayal["Color"] = "green"

        portrayal["Layer"] = 0
    
    # If the agent has no wealth, make it red
    else:
        
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1

    return portrayal

chart_currents = PieChartModule(
    [
        {"Label": "Wealthy Agents", "Color": "Green"},
        {"Label": "Non Wealthy Agents", "Color": "Red"},
    ],

    data_collector_name="datacollector_currents",

)

wealthiest_agent = ChartModule(
    [
        {"Label": "Wealthiest Agent", "Color": "Purple"},
    ],

    data_collector_name="datacollector_wealthiest_agent",

)

gini = ChartModule(
    [
        {"Label": "Gini", "Color": "Blue"},
    ],

    data_collector_name="datacollector_gini"
)

# create the grid with the initial values
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(FinancialModel, 
                    [grid, wealthiest_agent, gini, chart_currents, CustomCSS()],
                    "Financial Model", 
                    simulation_params,
                    8523)

server.launch()
