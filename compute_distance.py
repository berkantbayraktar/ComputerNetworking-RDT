#! /usr/bin/python

import re
import sys

from diff_match_patch import diff_match_patch

def print_colored(text, color):
    colors = {'red':'\033[91m', 'green':'\033[92m', 'blue':'\033[94m', 'default':'\033[0m'}
    clr = colors.get(color, '')
    sys.stdout.write(clr + text + colors['default'])

def print_diffs(diffs):
    for diff in diffs:
        if diff[0] == 0:
            print_colored(diff[1], 'green')
        elif diff[0] == -1:
            print_colored(diff[1], 'blue')
        else: # diff[0] == 1
            print_colored(diff[1], 'red')

def remove_space(diffs):
    newdiffs = []
    for diff in diffs:
        if diff[0] == 0:
            newdiffs.append(diff)
        else:
            # remove all shape within a string
            newdiff = re.sub(r'\s', '', diff[1])
            newdiffs.append((diff[0], newdiff))
    return newdiffs

def compute_diffs(original_file, modified_file):
    # read files
    original_f = open(original_file)
    original = original_f.read()
    original_f.close()
    modified_f = open(modified_file)
    modified = modified_f.read()
    modified_f.close()
    # compute the diff and distance
    dmp = diff_match_patch()
    diffs = dmp.diff_main(original, modified)
    diffs = remove_space(diffs)
    distance = dmp.diff_levenshtein(diffs)
    return distance, diffs


def usage(argv):
    print 'usage: %s <lab-file> <modified-file> [-v]' % argv[0]

def main(argv):
    if len(argv) < 3:
        usage(argv)
        return 1
    original_file = argv[1]
    modified_file = argv[2]
    verbose = len(argv) == 4 and argv[3] == '-v'
    try:
        distance, diffs = compute_diffs(original_file, modified_file)
        if verbose:
            print 'Edit distance between %s and %s is %d' % \
                    (original_file, modified_file, distance)
            print 
            print 'Combined text:'
            print_diffs(diffs)
        else:
            print distance
    except Exception, e:
        sys.stderr.write(str(e) + '\n')
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
