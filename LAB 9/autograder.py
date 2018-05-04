import sys
import kmeans
from math import *

def grade1():
    print '='*20 + ' TASK 1 ' + '='*20
    testcases = {
        'distance_euclidean': [
            (((2,2), (2,2)), 0),
            (((0,0), (0,1)), 1),
            (((1,0), (0,1)), sqrt(2)),
            (((0,0), (0,-1)), 1),
            (((0,0.5), (0,-0.5)), 1)
        ],
        'distance_manhattan': [
            (((2,2), (2,2)), 0),
            (((0,0), (0,1)), 1),
            (((1,0), (0,1)), 2),
            (((0,0), (0,-1)), 1),
            (((0,0.5), (0,-0.5)), 1)
        ],
        'iteration_one': [
            (([(i,i) for i in range(5)], [(1,1),(2,2),(3,3)], kmeans.distance_euclidean), [(0.5, 0.5), (2.0, 2.0), (3.5, 3.5)]),
            (([(i+1,i*2.3) for i in range(5)], [(5,1),(-1,2),(3,6)], kmeans.distance_euclidean), [(5, 1), (1.5, 1.15), (4.0, 6.8999999999999995)])
        ],
        'hasconverged': [
            (([(i,i*2,i*3) for i in range(5)], [(i,i*2,i*3+0.01) for i in range(5)], 0.01), True),
            (([(i,i*2,i*3) for i in range(5)], [(i,i*2,i*3+0.01) for i in range(5)], 0.002), False)
        ],
        'iteration_many': [
            (([(i,i) for i in range(3)], [(1,1),(2,2)], kmeans.distance_euclidean, 3, 0.01), [[(1, 1), (2, 2)], [(0.5, 0.5), (2.0, 2.0)], [(0.5, 0.5), (2.0, 2.0)]]),
            (([(i+1,i*2.3) for i in range(3)], [(5,1),(-1,2)], kmeans.distance_euclidean, 5, 0.01), [[(5, 1), (-1, 2)], [(3.0, 4.6), (1.5, 1.15)], [(3.0, 4.6), (1.5, 1.15)]])
        ],
        'performance_SSE': [
            (([(0,i) for i in range(10)], [(0,0), (0,5), (0,10)], kmeans.distance_euclidean), 20),
            (([(0,i) for i in range(10)], [(0,0), (0,5), (0,6), (0,10)], kmeans.distance_euclidean), 16),
            (([(0,i) for i in range(10)], [(0,50), (-2,5.8), (3,6.1), (0.5,10)], kmeans.distance_euclidean), 121.82)
        ]
    }
    grade = 0
    passedAll = True
    for function in testcases:
        passed = True
        for inp, out in testcases[function]:
            ret = getattr(kmeans,function)(*inp)
            if ret != out:
                print 'Function {} failed a testcase.\n\tInput: {}\n\tExpected return: {}\n\tRecieved return: {}\n'.format(function, str(inp)[1:-1], out, ret)
                passed = False
        print '  {}  Function {}'.format([u'\u2718', u'\u2713'][passed].encode('utf8'), function)
        print '-'*30
        grade += passed
        if not passed:
            passedAll = False
    
    grade *= 0.5

    print 'grade: {}'.format(grade)
    print ''
    return grade

def grade2():
    print '='*20 + ' TASK 2 ' + '='*20
    print 'This task is manually graded. Answer it in the file solutions.txt\n'
    return 0

def grade3():
    print '='*20 + ' TASK 3 ' + '='*20
    grade = 0
    # Test kmeans++.
    data = [(i,i) for i in range(5)]
    ret = kmeans.initialization_kmeansplusplus(data, kmeans.distance_euclidean, 3)
    passed = sum([1 for i in ret if i not in data]) == 0
    if len(ret) != 3:
        passed = 0
    if passed:
        grade = 1
    else:
        grade = 0
    if not passed:
        print 'Function initialization_kmeansplusplus failed a testcase.\n\tInput: {}\n\tExpected return: All cluster centers must come from data points.\n\tRecieved return: {}\n'.format((data, 3), ret)
        passedAll = False
    print '  {}  Function initialization_kmeansplusplus'.format([u'\u2718', u'\u2713'][passed].encode('utf8'))
    print "NOTE: The autograder doesn't check for correct implementation of this function.\nYour marks depend on whether the TAs are able to understand your code and establish its correctness."
    print '-'*30

    print "\nNOTE: This task has an additional manually graded question worth 2 marks. Answer it in solutions.txt\n"
    print 'grade: {}'.format(grade)
    print ''
    return grade

def grade4():
    print '='*20 + ' TASK 4 ' + '='*20
    data = kmeans.readfile('datasets/mnist.csv')
    labels = [int(i[0]) for i in kmeans.readfile('datasets/mnistlabels.csv')]

    means = kmeans.readfile('mnistmeans.txt')
    k = 10
    s = 0
    for index, point in enumerate(data):
        dlist = [kmeans.distance_euclidean(point, center) for center in means]
        pred = kmeans.argmin(dlist)
        s +=  labels[index] == pred
    accuracy = s/5000.0
    print 'Accuracy acieved: {}%'.format(accuracy*100)
    if accuracy >= 0.5:
        grade = 2
    elif accuracy >= 0.4:
        grade = 1
    else:
        grade = 0
    print 'grade: {}'.format(grade)
    print ''
    return grade

def gradeall(loc):
    print '='*48 + '\nFINAL GRADE: {}\n\n'.format(sum([loc['grade' + str(i)]() for i in range(1,5)]))

if len(sys.argv) < 2:
    print 'usage:\npython autograder.py [task-number]\npython autograder.py all'
    sys.exit(1)
print ''
if sys.argv[1].lower() == 'all':
    gradeall(locals())
else:
    locals()['grade' + str(int(sys.argv[1]))]()
