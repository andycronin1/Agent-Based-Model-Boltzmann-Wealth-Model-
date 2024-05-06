#Agent Based Model of the Boltzmann wealth model

#Background: Agents are the individual entities that act in the model. It is a good modeling practice to make certain each Agent can be uniquely identified.

#Model-specific information: Agents are the individuals that exchange money, in this case the amount of money an individual agent has is represented as wealth. Additionally, agents each have a unique identifier.

import mesa
import matplotlib as mp


#function to compute the the model’s Gini Coefficient, a measure of wealth inequality.        
def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

#Building a class of an agent 
class MoneyAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # Create the agent's variable and set the initial values.
        self.wealth = 1
                
    #Move agent method and move all neighbouring elememts      
    #Using moore and not von neumann  
    #Not including centre cell in the neighbours
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
  
    #Adding method for getting all the other agents present in a cell, and giving one of them some mone    
    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        cellmates.pop(
            cellmates.index(self)
        )  
        # Ensure agent is not giving money to itself
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1
            if other == self:
                print("I JUST GAVE MONEY TO MYSELF!")
            
    def step(self):
            # The agent's step method goes here.
            #Moving agent
            self.move()
            #giving money to another agent if money is more than 0
            if self.wealth > 0:
                self.give_money()
                
#Builidng a class of a model 
class MoneyModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        #Creating scheduler and adding it to the model
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            # Add the agent to the scheduler
            self.schedule.add(a)
            
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            
            #At every step of the model, the datacollector will collect and store the model-level current Gini coefficient, 
            #as well as each agent’s wealth, associating each with the current step.
            self.datacollector = mesa.DataCollector(
                model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        )
            
    def step(self):
        """Advance the model by one step."""
        
        #Calling data collector and collecting gini coefficient
        self.datacollector.collect(self)
        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()