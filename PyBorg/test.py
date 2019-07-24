import time
from pyborg import BorgMOEA
from platypus import DTLZ2, NSGAII

if __name__ == "__main__":
    problem = DTLZ2(3)
    
    start_time = time.time()
    borg = BorgMOEA(problem, epsilons=0.1)
    borg.run(10000)
    print("Borg:", time.time()-start_time)
    
    start_time = time.time()
    nsgaii = NSGAII(problem)
    nsgaii.run(10000)
    print("NSGA-II:", time.time()-start_time)
    
    # plot the results using matplotlib
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([s.objectives[0] for s in nsgaii.result],
               [s.objectives[1] for s in nsgaii.result],
               [s.objectives[2] for s in nsgaii.result],
               color="red")
    ax.scatter([s.objectives[0] for s in borg.result],
               [s.objectives[1] for s in borg.result],
               [s.objectives[2] for s in borg.result],
               color="blue")
    plt.show()