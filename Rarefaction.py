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

            # We found the right rank!
            # Check to see if it already exists in the dictory:
            if rank in dictionary:
                dictionary[rank] += 1

            else:
                dictionary[rank] = 1


"""
# =============================================================================

GenerateRarefaction

# =============================================================================
"""
def generateRarefaction(inputLocation, outputFile, label, samplingRates):

    # Open the file.
    inputFile = open(inputLocation, 'r')

    # Initialize the dictionaries.
    dictionaries = []

    for samplingRate in samplingRates:

        dictionaries.append({})

    # Populate the dictionaries with a specific random sampling rate.
    for line in inputFile:

        # Operate on each sampling rate independently.
        for i in range(0, len(samplingRates)):

            number = random.random() # Generate a random number (each time!)

            # Do we add the line to the sub sample?
            # Include the read if its sampling rate is greater than number.
            if number <= samplingRates[i]:

                tokens = line.split("\t")
                read = tokens[0].strip()
                classification = tokens[1].strip()

                rankings = classification.split("|")

                updateDictionary(dictionaries[i], rankings, label)

    # Close input file.
    inputFile.close()

    # Report the results.
    for i in range(0, len(samplingRates)):
        outputFile.write(str(len(dictionaries[i])))

        # Do we need to write a comma?
        if i < (len(samplingRates) - 1):  # There's another item following.
            outputFile.write(",")
        # Do we need the final end line?
        else:
            outputFile.write("\n")


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

    # Check the input file.
    if not os.path.isfile(inputLocation):
        raise RuntimeError(
            "ERROR: Could not open input file: " + inputLocation + "\n")

    # Check the rate is not within bounds.
    if (rate <= 0 or rate > 1):
        raise RuntimeError(
            "ERROR: The rate is not in range (0, 1]: " + str(rate) + "\n")

    # Open the output file.
    outputFile = open(outputLocation, 'w')

    samplingRates = []
    samplingPoints = int(1 / float(rate))

    for i in range(1, (samplingPoints + 1)):    # +1 to shift off 0

        samplingRates.append(i * rate)

    # Generate rarefaction data for each label.

    if "d" in labels:
        outputFile.write("Domain\n")
        generateRarefaction(inputLocation, outputFile, "d", samplingRates)

    if "p" in labels:
        outputFile.write("Phylum\n")
        generateRarefaction(inputLocation, outputFile, "p", samplingRates)

    if "c" in labels:
        outputFile.write("Class\n")
        generateRarefaction(inputLocation, outputFile, "c", samplingRates)

    if "o" in labels:
        outputFile.write("Order\n")
        generateRarefaction(inputLocation, outputFile, "o", samplingRates)

    if "f" in labels:
        outputFile.write("Family\n")
        generateRarefaction(inputLocation, outputFile, "f", samplingRates)

    if "g" in labels:
        outputFile.write("Genus\n")
        generateRarefaction(inputLocation, outputFile, "g", samplingRates)

    if "s" in labels:
        outputFile.write("Species\n")
        generateRarefaction(inputLocation, outputFile, "s", samplingRates)

    # Close output file.
    outputFile.close()

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



