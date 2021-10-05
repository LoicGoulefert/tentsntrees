# Tents and trees solver

Solving the Tents and Trees puzzle game ([Android download](https://play.google.com/store/apps/details?id=com.frozax.tentsandtrees&hl=en_US), 
[iOS download](https://apps.apple.com/app/tents-and-trees-puzzles/id1279378379)) using a constraint satisfaction problem solver.

The goal of this puzzle is to fill the grid with tents and grass. The rules are the following:
- Each tree must have a tent next to it
- Two tents cannot touch (even in diagonal)
- Every cell that is not a tent must be grass
- Numbers on the edge of the grid specify how many tents there is on each row / column


![Original application instance](img/tentsntrees_original.png)

*Original application screenshot.*


![Output example](img/solved_7x7.png)

*Output example of this program. Purple = tree, red = tent, green = grass.*


## Installation

This project is using python 3.6.9, and has been tested in an Ubuntu 18.04 environment.

```
git clone https://github.com/LoicGoulefert/tentsntrees.git
cd tentsntrees
pip install -r requirements.txt
``` 


## Usage

```
usage: main.py [-h] [-gd GRID_DIMENSION]

optional arguments:
  -h, --help            show this help message and exit
  -gd GRID_DIMENSION, --grid-dimension GRID_DIMENSION
                        specify the grid dimension
```


For example, the command `python main.py -gd 10` will solve and display a random 10x10 grid.


## Files

- `src/main.py`: entry point
- `src/grid.py`: grid object definition
- `src/interface.py`: PyGame GUI
- `src/solver.py`: CSP Model and solver
