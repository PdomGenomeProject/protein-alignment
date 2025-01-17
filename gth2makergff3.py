#!/usr/bin/env python
#
# -----------------------------------------------------------------------------
# Copyright (c) 2012-2015   Daniel Standage <daniel.standage@gmail.com>
# Copyright (c) 2012-2015   Indiana University
#
# This file is part of the Polistes dominula genome project and is licensed
# under the Creative Commons Attribution 4.0 International License.
# -----------------------------------------------------------------------------
import re
import sys

# Usage: gth2makergff3 < in.gsq > out.gff3

idcounts = {}
print "##gff-version   3"
skip = False
for line in sys.stdin:
    line = line.rstrip()
    if not line.startswith("MATCH") and not line.startswith("PGS_"):
        continue

    if line.startswith("MATCH"):
        match_values = line.split("\t")
        similarity = float(match_values[3])
        coverage = float(match_values[5])
        if similarity < 0.5 or coverage < 0.5:
            skip = True
            continue

    matches = re.search("PGS_(.+)([+-])_(.+)([+-])\s\((.+)\)", line)
    if not matches:
        continue

    if skip:
        skip = False
        continue

    id = matches.group(3)
    if id not in idcounts:
        idcounts[id] = 0
    idcounts[id] += 1
    uid = "%s.%d" % (id, idcounts[matches.group(3)])

    alignparts = matches.group(5).split(",")
    start = alignparts[0].split("  ")[0]
    end = alignparts[-1].split("  ")[1]
    if matches.group(2) == '-':
        start, end = end, start
    print "%s\tGenomeThreader\ttranslated_nucleotide_match\t%s\t%s\t.\t%c\t.\tID=%s.match;Name=%s" % (matches.group(1), start, end, matches.group(2), uid, id)

    template = "%s\tGenomeThreader\tmatch_part\t%%s\t%%s\t.\t%c\t.\tID=%s;Parent=%s.match" % (
        matches.group(1), matches.group(2), uid, uid)
    for alignpart in alignparts:
        coords = alignpart.split("  ")
        if matches.group(2) == '-':
            coords[0], coords[1] = coords[1], coords[0]
        print template % (coords[0], coords[1])
