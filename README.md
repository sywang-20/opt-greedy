# **Code for Nondominated Solution-based Multi-objective Evolutionary Greedy Algorithm**

1. greedy\
the code which introduces the evolutionary mechanism into the greedy algorithm
2. greedy-original\
the code which is the original greedy algorithm
3. nsga_baseline\
the NSGA-II code


# **Experiment design**
## main idea
- In this paper, we aim to propose a new algorithm, i.e., introduce the evolutionary mechanism into the original greedy algorithm to scale up the greedy algorithm so that it can be applied to large-scale problems.
- Therefore, in this paper, we will focus on the synthetic case to compare the algorithms. After proving the superiority of the new algorithm, we will apply it to the real-world case (HK sewage network). *This is the main difference from the previous paper.*
  
## synthetic case  
### *algorithm comparison and parameter sensitivity*
*RQ 1: how does the evolutionary greedy algorithm perform compared with the original greedy algorithm on the networks with different sizes?*

can also consider other greedy family algorithms

*RQ 2: how does the parameter 'new_plans' affect the performance of the evolutionary greedy algorithm?*

test different values of 'new_plans' in the evolutionary greedy algorithm, and compare the performance of the algorithm with the original greedy algorithm (measure it using the difference between evolutionary and original greedy)

**evolutionary greedy**
- at each step:
  1. produce 2，3，4，5... new plans for one plan
  2. keep 20 plans
   

**original greedy**
- at each step:
    1. iterate all uncovered manholes
    2. keep 20 plans

<!-- ### 2. Parameter sensitivity
*RQ: how the parameter 'new_plans' affect the performance of the evolutionary greedy algorithm?*

test different values of 'new_plans' in the evolutionary greedy algorithm, and compare the performance of the algorithm with the original greedy algorithm (measure it using the difference between evolutioary and original greedy)

**evolutionary greedy**
- at each step:
  1. produce 20, 30, 40, 50 new plans for one plan
  2. keep 20 plans -->


## real-world case
*RQ 3: how can the evolutionary greedy algorithm be applied to solve the real-world problem?*


