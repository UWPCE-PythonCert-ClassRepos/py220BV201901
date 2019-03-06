"""
check good works the same, and is faster
"""

import poor_perf as p
import good_perf as g

def test_assess_preformance():
    """ compare """
    poor = p.analyze('exercise.csv')
    good = g.analyze('exercise.csv')
    poor_elapsed = poor[1] - poor[0]
    good_elapsed = good[1] - good[0]
    assert good_elapsed < poor_elapsed
    assert poor[2] == good[2]
    assert poor[3] == good[3]

    print(f'poor: {poor}\n')
    print(f'poor_elapsed: {poor_elapsed}\n')

    print(f'good: {good}\n')
    print(f'good_elapsed: {good_elapsed}\n')

    assert False # DKA added to see stdout
