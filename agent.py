from mesa import Agent

class FinancialAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, wealth, risk_aversion):
        super().__init__(unique_id, model)
        self.wealth = wealth
        self.risk_aversion = risk_aversion
        self.transactions = 0
    
    def step(self):
        self.move()
        if self.wealth > 0:
            self.trade()

    def trade(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            if self.get_strategy() == "Barter":
                self.barter_trade(other)
            elif self.get_strategy() == "Gift":
                self.gift_trade(other)
            else:
                self.give_money(other)
            
            self.transactions += 1
        
    def give_money(self, other):
        other.wealth += 1
        self.wealth -= 1
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def barter_trade(self, other):
        if other.wealth > 0:
            offer = self.random.randint(1, other.wealth)
            if offer > other.wealth:
                offer = other.wealth
            self.wealth -= offer
            other.wealth += offer

    def gift_trade(self, other):
        if other.wealth < self.wealth:
            gift = self.random.randint(1, self.wealth - other.wealth)
            print("Gift: ", gift)
            self.wealth -= gift
            other.wealth += gift
    
    def momentum_trade(self):
        if self.wealth <= 0:
            return

    def get_trust_level(self, other):
        trust_coefficient = 0.5
        if other.wealth > self.wealth:
            return trust_coefficient + trust_coefficient * (other.wealth - self.wealth) / self.wealth
        elif other.wealth < self.wealth:
            return trust_coefficient - trust_coefficient * (self.wealth - other.wealth) / self.wealth
        else:
            return trust_coefficient

    def get_risk_aversion(self):
        return self.risk_aversion

    def set_risk_aversion(self, risk_aversion):
        self.risk_aversion = risk_aversion
    
    def get_wealth(self):
        return self.wealth

    def get_transactions(self):
        return self.transactions

    def get_strategy(self):
        return self.model.strategy
