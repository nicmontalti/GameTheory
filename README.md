# Influence of probabilistic abstention on spatial cooperative games

This code was developed for the course _Controversies in Game Theory_ at ETH Zürich. It can be used to play the prisoner's dilemma game (or other games) in a 2D spatial environment, and look at the effects of optional (or probabilistic) abstention.

## Structure of the repository
```
.
├── README.md                                 # this file
├── game.py                                   # definition of the class Game
├── results.ipynb                             # Jupyter notebook used to generate the results
├── functions.py                              # some useful functions
├── data/                                     # raw data
    ├── *.npy
    ├── ...          
├── plots/                                    # rplots included in the report
    ├── *.npy
    ├── ...               
├── tex
    ├── Report.pdf                            # final report
    ├── ...

```
## The code
### Dependencies
- Python 3
- Numpy
- Matplotlib

### How to use the code
The file game.py can be used to run a simulation and see the evolution in real time. The file results.ipynb is useful to examine the results and make the plots.

To run a simulation the following parameters have to be specified:
- the payoffs: T, R, S, P and L, according to the table
```
                | Cooperate | Defect | Abstain |
    |-----------|-----------|--------|---------|
    | Cooperate | R, R      | S, T   | L, L    |
    | Defect    | T, S      | P, P   | L, L    |
    | Abstain   | L, L      | L, L   | L, L    |
```
- the noise: the probability to randomly changing strategy
- the type of game (normal, optional or with probabilistic abstention)

For the details about the meaning of the parameters, please refer to the report in the repository