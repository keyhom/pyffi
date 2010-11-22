"""Parse all FRAPS generated csv files and print summary info."""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007-2009, Python File Format Interface
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the Python File Format Interface
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****

import csv
import os
import sys

def mean(vec):
    """
    >>> mean([1, 2, 3, 4, 5])
    3.0
    """

    return float(sum(vec)) / len(vec)

def sd(vec):
    """
    >>> sd([1, 2, 3, 4, 5]) # doctest: +ELLIPSIS
    1.581138...
    """
    m = mean(vec)
    return (float(sum((v - m) ** 2 for v in vec)) / (len(vec) - 1)) ** 0.5

total = {}
folder = sys.argv[1]
for root, dirs, files in os.walk(folder):
    total[root] = {"Frames": [], "Time (ms)": [], "Min": [], "Max": [], "Avg": []}
    for name in files:
        if not name.endswith(".csv"):
            continue
        print("parsing {0}".format(name))
        with open(os.path.join(root, name), "rb") as csvfile:
            rows = csv.reader(csvfile)
            header = rows.next()
            numbers = rows.next()
            for name, num in zip(header, numbers):
                name = name.strip()
                total[root][name].append(float(num))

def summary(outfile):
    for root in sorted(total):
        if not total[root]["Frames"]:
            continue
        print >>outfile, root
        print >> outfile, "-" * len(root)
        print >> outfile
        print >>outfile, "summary of {0} tests:".format(len(total[root]["Frames"]))
        for name, vec in total[root].iteritems():
            print >> outfile, "{0:10}: {1:10.3f} +- {2:10.3f}".format(
                name,
                mean(vec),
                1.96 * sd(vec) / (len(vec) ** 0.5))
        print >> outfile

summary(sys.stdout)
with open(os.path.join(folder, "summary.txt"), "w") as outfile:
    summary(outfile)

#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()