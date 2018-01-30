# Introduction #

This software generates rarefaction data from Kraken output. The software
organizes reads into subsamples and reports the number of taxa present within
each subsample for all principal classification ranks. The output of this
software  is in csv format.

# Release #

Krakefaction 0.2.0

# Installation #

This software is compatible with Python 2.7 and Python 3. The following may
check your Python version:

```bash
python --version
```

The user must insure the following requirements are met:

* Python 2.7 or Python 3
* virtualenv
* pip

The software will be installed using pip into its own Python virtual
environment. The following will install the software locally into the source
directory and will not require security privileges:

```bash
krakefaction/INSTALL.sh
```

Alternatively, you may specify an install location, PREFIX, such as
/usr/local/. The software will create the directories PREFIX/lib and
PREFIX/bin. This may require security privileges:


```bash
krakefaction/INSTALL.sh PREFIX
```

# Running Krakefaction #

Krakefaction's command line arguments can be found by running:

```bash
krakefaction --help
```

A simple example of running Krakefaction:

```bash
krakefaction -u untranslated.tab -t translated.tab -o output.csv
```

# Contact #

**Eric Marinier**: eric.marinier@canada.ca

# Legal #

Copyright Government of Canada 2018

Written by: Eric Marinier, National Microbiology Laboratory,
    Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

