Diagonal Sudoku Solver
===============================
In this project, I will write code to implement two extensions to already implemented sudoku solver. The first one will be to apply the technique called "naked twins." The second one will be to modify the existing code to solve a diagonal sudoku. To complete this project, I will use mostly constraint propagation and depth-first search. This project is part of [Artificial Intelligence Nanodegree](https://www.udacity.com/ai) program, from Udacity.

### Questions:
###### Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *We use constraint propagation in some steps. First, we look for naked twins just in boxes that have presented two possible values, reducing the search space. Then, we walk through each unit of the remaining boxes to check if there was another box with the same value. Finally, when we find such boxes, we eliminate their values from the other boxes in the unit.*

###### Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *We have used constraint propagation to compose several strategies when solving sudoku problems, as the only choice. We also have used when we have walked through each peer or unit related to each box checking these strategies. So, apart from those steps, we just have to add the diagonals as units to solve diagonal sudoku.*

### Install
This project requires **Python 3** and the following Python libraries installed:
- [Pygames](https://www.pygame.org/wiki/GettingStarted)
- [Unittest](https://docs.python.org/2/library/unittest.html)


### Run
In a terminal or command window, if you have pygames installed, navigate to the top-level project directory 'Sudoku/' (that cointains this README) and run the following command:

```shell
$ python solution.py
```

A window should pop up after that with an animation of the game being solved.


### Reference
1. [Udacity original code](https://github.com/udacity/AIND-Sudoku)

### License
The contents of this repository are covered under the [MIT License](LICENSE.md).
