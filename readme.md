# DTPOG

(still developing ... )

We propose a framework for *Discrete Time Partially Observed (Markov) Game*, where gamestate can only be partially observed. 

### Modeling
The game can be modeled as an automaton with probability, or a chain of Markov stochastic process.
$${\text{Game}} = \{\boldsymbol{S},\tau\in\mathbb{N+},\eta:I\times\boldsymbol{S}\mapsto\boldsymbol{S},P_{|\boldsymbol{S}|\times|\boldsymbol{S}|},\delta:\boldsymbol{S}\times\mathbb{N+}\mapsto\{0,1,2\}\}$$
where $I$ is the player instruction, $\eta$ maps the player instruction with current state to a new state;<br>

$P$ is the transition matrix, or transition function of the game.<br>

$\tau$ is the discrete time, and $\delta$ maps time with game state to the result of game, which is the only part that conserns time, and does not affect other arguments.<br>

What makes the game interesting is, that the game is a stochastic process with **hidden state space**, which needs to be inferred from observation. We take a step further that **to observe** itself is an action applied by agent that will affect game. It costs to get information.<br>

From another perspective, the agent who plays the game, along with the game, is considered as a part of an entire system. The agent plays the role of a control unit, which should operate properly to make the system as reliable as possible.



### Project Structure

- [ ] todo



### Framework



### Demo Game 

#### FNAF1





