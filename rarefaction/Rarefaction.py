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

# CONSTANTS

CLASSIFIED = "C"

# DEFAULTS #

DEFAULT_RATE = 0.05

# ARGUMENTS #

LONG = "--"
SHORT = "-"

# REQUIRED ARGUMENTS #

TRANSLATED = "translated"
TRANSLATED_LONG = LONG + TRANSLATED
TRANSLATED_SHORT = SHORT + "t"
TRANSLATED_HELP = "The file name of the input Kraken translated reads."

UNTRANSLATED = "untranslated"
UNTRANSLATED_LONG = LONG + UNTRANSLATED
UNTRANSLATED_SHORT = SHORT + "u"
UNTRANSLATED_HELP = "The file name of the input untranslated Kraken reads. \
    These may be filtered or "

OUTPUT = "output"
OUTPUT_LONG = LONG + OUTPUT
OUTPUT_SHORT = SHORT + "o"
OUTPUT_HELP = "The file name of the output rarefaction data."

# OPTIONAL ARGUMENTS #

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

SAMPLING RATE CLASS

# =============================================================================
"""
class SamplingRate:

    DOMAIN = "d"
    PHYLUM = "p"
    CLASS = "c"
    ORDER = "o"
    FAMILY = "f"
    GENERA = "g"
    SPECIES = "s"

    """
    # =============================================================================

    CONSTRUCTOR

    # =============================================================================
    """
    def __init__(self, rate):

        self.rate = rate

        self.domainDictionary = {}
        self.phylumDictionary = {}
        self.classDictionary = {}
        self.orderDictionary = {}
        self.familyDictionary = {}
        self.generaDictionary = {}
        self.speciesDictionary = {}

    """
    # =============================================================================

    UPDATE DICTIONARIES

    # =============================================================================
    """
    def updateDictionaries(self, rankings):

        self.updateDictionary(self.domainDictionary, rankings, self.DOMAIN)
        self.updateDictionary(self.phylumDictionary, rankings, self.PHYLUM)
        self.updateDictionary(self.classDictionary, rankings, self.CLASS)
        self.updateDictionary(self.orderDictionary, rankings, self.ORDER)
        self.updateDictionary(self.familyDictionary, rankings, self.FAMILY)
        self.updateDictionary(self.generaDictionary, rankings, self.GENERA)
        self.updateDictionary(self.speciesDictionary, rankings, self.SPECIES)

    """
    # =============================================================================

    UPDATE DICTIONARY

    # =============================================================================
    """
    def updateDictionary(self, dictionary, rankings, label):

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
def generateRarefaction(untranslatedLocation, translatedLocation, outputFile, samplingRates):

    # Open the files.
    untranslatedFile = open(untranslatedLocation, 'r')
    translatedFile = open(translatedLocation, 'r')

    # Initialize.
    numberOfReads = []

    for samplingRate in samplingRates:

        numberOfReads.append(0)

    # Iterate over all the reads in the untranslated file.
    for untranslatedLine in untranslatedFile:

        number = random.random() # Generate a random number once per read!
        # We generate this random number once because we want all reads to
        # be in all sampling rate dictionaries that are "bigger" (have a
        # higher probability).

        # Is the read classified?
        # We only want to do this work once for all the sampling rates!
        if untranslatedLine[0] == CLASSIFIED:

            # Advance the translated file to find the translation.
            translatedLine = translatedFile.readline()

            # Tokenize the translation.
            tokens = translatedLine.strip().split()
            read = tokens[0].strip()
            classification = tokens[1].strip()

            rankings = classification.split("|")

        # Operate on each sampling rate:
        for i in range(0, len(samplingRates)):

            # Do we add the read to the subsample (classified and unclassied)?
            # Include the read if its sampling rate is greater or equal.
            if number <= samplingRates[i].rate:

                numberOfReads[i] += 1 # Increment the number of reads.

                # Is the read classified?
                # Update the dictionaries.
                if untranslatedLine[0] == CLASSIFIED:
                    samplingRates[i].updateDictionaries(rankings)

    # Close input files.
    untranslatedFile.close()
    translatedFile.close()

    writeResults(samplingRates, numberOfReads, outputFile)

"""
# =============================================================================

WRITE RESULTS

# =============================================================================
"""
def writeResults(samplingRates, numberOfReads, outputFile):

    last = len(samplingRates) - 1

    # Rates
    outputFile.write("rates,")
    for i in range(0, len(samplingRates) - 1):
        outputFile.write(str(samplingRates[i].rate) + ",")
    outputFile.write(str(samplingRates[last].rate)) # last
    outputFile.write("\n")

    # Number of reads in each subsample:
    outputFile.write("reads,")
    for i in range(0, len(numberOfReads) - 1):
        outputFile.write(str(numberOfReads[i]) + ",")
    outputFile.write(str(numberOfReads[len(numberOfReads) - 1])) # last
    outputFile.write("\n")

    # Domains
    outputFile.write("domains,")
    for i in range(0, len(samplingRates) - 1):
        outputFile.write(str(len(samplingRates[i].domainDictionary)) + ",")
    outputFile.write(str(len(samplingRates[last].domainDictionary))) # last
    outputFile.write("\n")

    # Phylums
    outputFile.write("phylums,")
    for i in range(0, len(samplingRates) - 1):
        outputFile.write(str(len(samplingRates[i].phylumDictionary)) + ",")
    outputFile.write(str(len(samplingRates[last].phylumDictionary))) # last
    outputFile.write("\n")

    # Classes
    outputFile.write("classes,")
    for i in range(0, len(samplingRates) - 1):
        outputFile.write(str(len(samplingRates[i].classDictionary)) + ",")
    outputFile.write(str(len(samplingRates[last].classDictionary))) # last
    outputFile.write("\n")

    # Orders
    outputFile.write("orders,")
    for i in range(0, len(samplingRates) - 1):
        outputFile.write(str(len(samplingRates[i].orderDictionary)) + ",")
    outputFile.write(str(len(samplingRates[last].orderDictionary))) # last
    outputFile.write("\n")

    # Families
    outputFile.write("families,")
    for i in range(0, len(samplingRates) - 1):
        outputFile.write(str(len(samplingRates[i].familyDictionary)) + ",")
    outputFile.write(str(len(samplingRates[last].familyDictionary))) # last
    outputFile.write("\n")

    # Genera
    outputFile.write("genera,")
    for i in range(0, len(samplingRates) - 1):
        outputFile.write(str(len(samplingRates[i].generaDictionary)) + ",")
    outputFile.write(str(len(samplingRates[last].generaDictionary))) # last
    outputFile.write("\n")

    # Species
    outputFile.write("species,")
    for i in range(0, len(samplingRates) - 1):
        outputFile.write(str(len(samplingRates[i].speciesDictionary)) + ",")
    outputFile.write(str(len(samplingRates[last].speciesDictionary))) # last
    outputFile.write("\n")


"""
# =============================================================================

RUN

# =============================================================================
"""
def run(untranslatedLocation, translatedLocation, outputLocation, rate):

    # Check the untranslated file.
    if not os.path.isfile(untranslatedLocation):
        raise RuntimeError(
            "ERROR: Could not open input file: " + untranslatedLocation + "\n")

    # Check the translated file.
    if not os.path.isfile(translatedLocation):
        raise RuntimeError(
            "ERROR: Could not open input file: " + translatedLocation + "\n")

    # Check for optional values and set if necessary.
    if not rate:
        rate = DEFAULT_RATE

    # Check the rate is not within bounds.
    if (rate <= 0 or rate > 1):
        raise RuntimeError(
            "ERROR: The rate is not in range (0, 1]: " + str(rate) + "\n")

    # Open the output file.
    outputFile = open(outputLocation, 'w')

    # Initialize the sampling rates (as classes with a rate variable):
    samplingRates = []
    samplingPoints = int(1 / float(rate))

    for i in range(1, (samplingPoints + 1)):    # +1 to shift start off 0 to 1

        samplingRates.append(SamplingRate(i * rate))

    generateRarefaction(untranslatedLocation, translatedLocation, outputFile, samplingRates)

    # Close output file.
    outputFile.close()

"""
# =============================================================================

PARSE

# =============================================================================
"""
def parse(parameters):

    untranslatedLocation = parameters.get(UNTRANSLATED)
    translatedLocation = parameters.get(TRANSLATED)
    outputLocation = parameters.get(OUTPUT)
    rate = parameters.get(RATE)

    run(untranslatedLocation, translatedLocation, outputLocation, rate)

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
        UNTRANSLATED_SHORT,
        UNTRANSLATED_LONG,
        dest=UNTRANSLATED,
        help=UNTRANSLATED_HELP,
        type=str, required=True)

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
        RATE_SHORT,
        RATE_LONG,
        dest=RATE,
        help=RATE_HELP,
        type=float)

    args = parser.parse_args()
    parameters = vars(args)

    print("Rarefaction v" + str(__version__) + "\n")
    parse(parameters)

    print("\nComplete!")


"""
# =============================================================================
# =============================================================================
"""
if __name__ == '__main__':

    main()



