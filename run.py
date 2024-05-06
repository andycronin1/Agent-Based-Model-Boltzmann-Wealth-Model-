from money_model import MoneyModel
import seaborn as sns
import numpy as np

model = MoneyModel(100, 10, 10)
for i in range(20):
    model.step()
    
#Using seaborn and numpy to visualize the number of agents residing in each cell. 
#To do that, we create a numpy array of the same size as the grid, filled with zeros. 
#Then we use the grid object’s coord_iter() feature, which lets us loop over every cell in the grid, giving us each cell’s positions and contents in turn.


##Plotting agents and movement of money as a heat map for final step
# agent_counts = np.zeros((model.grid.width, model.grid.height))
# for cell_content, (x, y) in model.grid.coord_iter():
#     agent_count = len(cell_content)
#     agent_counts[x][y] = agent_count
# # Plot using seaborn, with a size of 5x5
# g = sns.heatmap(agent_counts, cmap="viridis", annot=True, cbar=False, square=True)
# g.figure.set_size_inches(4, 4)
# g.set(title="Number of agents on each cell of the grid");

gini = model.datacollector.get_model_vars_dataframe()
# Plot the Gini coefficient over time
g = sns.lineplot(data=gini)
g.set(title="Gini Coefficient over Time", ylabel="Gini Coefficient");

#Putting Agent Wealth into a dataframe
agent_wealth = model.datacollector.get_agent_vars_dataframe()

#Plotting a histogram of the wealth of agents at the last step
last_step = agent_wealth.index.get_level_values("Step").max()
end_wealth = agent_wealth.xs(last_step, level="Step")["Wealth"]
# Create a histogram of wealth at the last step
g = sns.histplot(end_wealth, discrete=True)
g.set(
    title="Distribution of wealth at the end of simulation",
    xlabel="Wealth",
    ylabel="Number of agents",
);


# Get the wealth of given agent over time
one_agent_wealth = agent_wealth.xs(14, level="AgentID")
# Plot the wealth of agent 14 over time
g = sns.lineplot(data=one_agent_wealth, x="Step", y="Wealth")
g.set(title="Wealth of agent 14 over time");

#Plotting wealth of multiple agents over time
agent_list = [3, 14, 25]
# Get the wealth of multiple agents 
multiple_agents_wealth = agent_wealth[
    agent_wealth.index.get_level_values("AgentID").isin(agent_list)
]
# Plot the wealth of multiple agents
g = sns.lineplot(data=multiple_agents_wealth, x="Step", y="Wealth", hue="AgentID")
g.set(title="Wealth of agents 3, 14 and 25 over time");