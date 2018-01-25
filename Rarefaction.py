#!/usr/bin/env python

"""
# =============================================================================

Copyright Government of Canada 2018

Written by: Eric Marinier, Public Health Agency of Canada,
    National Microbiology Laboratory

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

# =============================================================================
"""

__version__ = '0.1.0'

import os
import argparse
import sys
import random


"""
# =============================================================================

GLOBALS

# =============================================================================
"""

PROGRAM_DESCRIPTION = "This program generates a rarefaction curve for Kraken \
    data."

PROGRAM_USAGE = "%(prog)s -t TRANSLATED -o OUTPUT"

# DEFAULTS #

DEFAULT_LABELS = "s"
DEFAULT_RATE = 0.05

# ARGUMENTS #

LONG = "--"
SHORT = "-"

# REQUIRED ARGUMENTS #

TRANSLATED = "translated"
TRANSLATED_LONG = LONG + TRANSLATED
TRANSLATED_SHORT = SHORT + "t"
TRANSLATED_HELP = "The file name of the input Kraken translated reads."

OUTPUT = "output"
OUTPUT_LONG = LONG + OUTPUT
OUTPUT_SHORT = SHORT + "o"
OUTPUT_HELP = "The file name of the output rarefaction data."

# OPTIONAL ARGUMENTS #

LABELS = "labels"
LABELS_LONG = LONG + LABELS
LABELS_SHORT = SHORT + "l"
LABELS_HELP = "The Kraken taxonomic labels for which to produce rarefaction \
    data. These labels are 'd','p','c','o','f','g','p', and 's'. These \
    labels should be provided as the comprising characters of a string. \
    Example: 'pogs' would produce output for the phylum, order, genus, and \
    species level."

RATE = "rate"
RATE_LONG = LONG + RATE
RATE_SHORT = SHORT + "r"
RATE_HELP = "The sampling rate in the range (0, 1]. Example: 0.1 will \
    generate 10 data points."

# Version number
VERSION = "version"
VERSION_LONG = LONG + VERSION
VERSION_SHORT = SHORT + "V"

"""
# =============================================================================

UPDATE DICTIONARY

# =============================================================================
"""
def updateDictionary(dictionary, rankings, label):

    for rank in rankings:

        if rank.startswith(str(label) + "_"):

            # we found the right rank!
            # check to see if it already exists in the dictory:

            if rank in dictionary:
                dictionary[rank] += 1

            else:
                dictionary[rank] = 1


"""
# =============================================================================

OPERATE

# =============================================================================
"""
def operate(inputLocation, label, samplingRates):

    # check input file
    if not os.path.isfile(inputLocation):
        raise RuntimeError(
            "ERROR: Could not open input file: " + inputLocation + "\n")

    inputFile = open(inputLocation, 'r')

    # initialize dictionaries
    dictionaries = []

    for samplingRate in samplingRates:

        dictionaries.append({})

    for line in inputFile:

        number = random.random() # generate a random number

        # include the current read in all subsampling rates greater than number
        for i in range(0, len(samplingRates)):

            # do we add the line to the sub sample?
            if number <= samplingRates[i]:

                tokens = line.split("\t")
                read = tokens[0].strip()
                classification = tokens[1].strip()

                rankings = classification.split("|")

                updateDictionary(dictionaries[i], rankings, label)

    # close input file
    inputFile.close()

    # report
    for i in range(0, len(samplingRates)):
        print str(samplingRates[i]) + " -- " + str(len(dictionaries[i]))


"""
# =============================================================================

RUN

# =============================================================================
"""
def run(inputLocation, outputLocation, labels, rate):

    # Check for optional values and set if necessary.
    if not labels:
        labels = DEFAULT_LABELS

    if not rate:
        rate = DEFAULT_RATE

    samplingRates = []
    samplingPoints = int(1 / float(rate))

    print samplingPoints

    for i in range(1, (samplingPoints + 1)):    # +1 to shift off 0

        samplingRates.append(i * rate)

    print samplingRates

    if "d" in labels:
        print "\nDomain"
        operate(inputLocation, "d", samplingRates)

    if "p" in labels:
        print "\nPhylum"
        operate(inputLocation, "p", samplingRates)

    if "c" in labels:
        print "\nClass"
        operate(inputLocation, "c", samplingRates)

    if "o" in labels:
        print "\nOrder"
        operate(inputLocation, "o", samplingRates)

    if "f" in labels:
        print "\nFamily"
        operate(inputLocation, "f", samplingRates)

    if "g" in labels:
        print "\nGenus"
        operate(inputLocation, "g", samplingRates)

    if "s" in labels:
        print "\nSpecies"
        operate(inputLocation, "s", samplingRates)

"""
# =============================================================================

PARSE

# =============================================================================
"""
def parse(parameters):

    inputLocation = parameters.get(TRANSLATED)
    outputLocation = parameters.get(OUTPUT)
    labels = parameters.get(LABELS)
    rate = parameters.get(RATE)

    run(inputLocation, outputLocation, labels, rate)

"""
# =============================================================================

MAIN

# =============================================================================
"""
def main():

    # --- PARSER --- #
    parser = argparse.ArgumentParser(
        description=PROGRAM_DESCRIPTION,
        usage=PROGRAM_USAGE)

    # --- VERSION --- #
    parser.add_argument(
        VERSION_SHORT,
        VERSION_LONG,
        action='version',
        version='%(prog)s ' + str(__version__))

    # --- REQUIRED --- #
    required = parser.add_argument_group("REQUIRED")

    required.add_argument(
        TRANSLATED_SHORT,
        TRANSLATED_LONG,
        dest=TRANSLATED,
        help=TRANSLATED_HELP,
        type=str, required=True)

    required.add_argument(
        OUTPUT_SHORT,
        OUTPUT_LONG,
        dest=OUTPUT,
        help=OUTPUT_HELP,
        type=str, required=True)

    # --- OPTIONAL --- #
    optional = parser.add_argument_group("OPTIONAL")

    optional.add_argument(
        LABELS_SHORT,
        LABELS_LONG,
        dest=LABELS,
        help=LABELS_HELP,
        type=str)

    optional.add_argument(
        RATE_SHORT,
        RATE_LONG,
        dest=RATE,
        help=RATE_HELP,
        type=float)

    args = parser.parse_args()
    parameters = vars(args)

    print("Rarefaction v" + str(__version__) + "\n")
    parse(parameters)


"""
# =============================================================================
# =============================================================================
"""
if __name__ == '__main__':

    main()



