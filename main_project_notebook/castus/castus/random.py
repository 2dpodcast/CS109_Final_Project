from __future__ import absolute_import
import random


strings = {
    'left_keys': 'qwertasdfgzxcvb',
    'right_keys': 'yuiophjklnm',
    'left_homerow': 'asdf',
    'right_homerow': 'jkl'
}

def randname(num_letters):
    """Generate random, easy to type letter sequences.

    This module solves the problem of finding unused names in crowded
    namespaces, and optimizes for ease of typing without requirement
    for meaningfulness.  Useful for establishing a top-level namespace
    name, bypassing the step of trying to figure out a name that
    hasn't been taken.
    """
    ret_ary = []
    for i in xrange(num_letters):
        key = (i % 2 == 0 and 'left_homerow' or 'right_homerow')
        s = strings[key]
        ret_ary.append(random.choice(s))

    return ''.join(ret_ary)
