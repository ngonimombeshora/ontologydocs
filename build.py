#!/usr/bin/env python3

import sys
import subprocess
from os import listdir
from os.path import isfile, join, splitext

pylodePath = "/Users/karl/Downloads/pyLODE-2.3/pylode/bin/pylode.sh"

ontologyFileEndings = ["owl", "rdf", "ttl", "nq"]

if (len(sys.argv) != 2):
    print("Usage: './build.py OntologyDirectory', e.g., './build.py 3.1.3'")
    sys.exit()

ontologyPath = sys.argv[1]

allFiles = [f for f in listdir(ontologyPath) if isfile(join(ontologyPath, f))]
ontologyFiles = [f for f in allFiles if splitext(f)[1].strip('.') in ontologyFileEndings]

for inputFile in ontologyFiles:
    fEnding = splitext(inputFile)[1]
    outputFileName = inputFile.replace(fEnding, ".html")
    subprocess.run([pylodePath, "-i", f"{ontologyPath}/{inputFile}", "-o", f"{ontologyPath}/{outputFileName}"])