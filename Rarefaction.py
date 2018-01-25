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


"""
# =============================================================================

GLOBALS

# =============================================================================
"""

PROGRAM_DESCRIPTION = "This program generates a rarefaction curve for Kraken \
    data."

PROGRAM_USAGE = "%(prog)s -t TRANSLATED -o OUTPUT"

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
                #print "updating " + str(rank)

            else:

                dictionary[rank] = 1
                #print "adding " + str(rank)


"""
# =============================================================================

OPERATE

# =============================================================================
"""
def operate(inputLocation):

    dictionary = {}

    # check input file
    if not os.path.isfile(inputLocation):
        raise RuntimeError(
            "ERROR: Could not open input file: " + inputLocation + "\n")

    inputFile = open(inputLocation, 'r')

    for line in inputFile:

        #print line

        tokens = line.split("\t")
        read = tokens[0].strip()
        classification = tokens[1].strip()

        #print read
        #print classification

        rankings = classification.split("|")

        #print rankings

        updateDictionary(dictionary, rankings, "s")

    # close input file
    inputFile.close()

    print len(dictionary)


"""
# =============================================================================

PARSE

# =============================================================================
"""
def parse(parameters):

    inputLocation = parameters.get(TRANSLATED)
    outputLocation = parameters.get(OUTPUT)

    operate(inputLocation)


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



