#!/bin/bash
#
# From https://www.reddit.com/r/adventofcode/comments/18qbsxs/comment/kexsobf/?utm_source=share&utm_medium=web2x&context=3
#
# Make sure: 
# 1. day25-visualise.sed exists:
#    1{x; /^$/i\
#    graph {
#    g;}
#    /:$/{ $a\
#    }
#    d;}
#    /:/{s/^\(...\): \(...\)\(.*\)/\1 -- \2\n\1:\3/; P; D;}
#
# 2. sudo apt install graphviz

# graph for test data
sed -f day25-visualise.sed ../data/day25-test.txt > day25-test-graph.dot ; neato -T svg day25-test-graph.dot > day25-test-graph.svg
open day25-test-graph.svg

# graph for real data
sed -f day25-visualise.sed ../data/day25.txt > day25-graph.dot ; neato -T svg day25-graph.dot > day25-graph.svg
open day25-graph.svg
