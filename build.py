#!/usr/bin/env python3

import sys
import subprocess
from os import listdir, remove
from os.path import isfile, join, splitext, isdir
from shutil import copytree
from rdflib import Graph
from rdflib.namespace import OWL, RDF

pylodePath = "bin/pyLODE-2.3/pylode/bin/pylode.sh"
owl2vowlPath = "bin/owl2vowl.jar"

ontologyFileEndings = ["owl", "rdf", "ttl", "nq"]

if (len(sys.argv) != 2):
    print("Usage: './build.py OntologyDirectory', e.g., './build.py 3.1.3'")
    sys.exit()

ontologyPath = sys.argv[1]

allFiles = [f for f in listdir(ontologyPath) if isfile(join(ontologyPath, f))]
ontologyFiles = [f for f in allFiles if splitext(f)[1].strip('.') in ontologyFileEndings]

# Copy webvowl skeleton
if not isdir(f"{ontologyPath}/webvowl"):
    copytree("webvowl", f"{ontologyPath}/webvowl")

# Set up unioned ontology graph for full
unionedOntology = Graph()
unionedOntology.parse(f"{ontologyPath}/full.rdf")

# The below is run offline in order for owl2vowl to not resolve URIs online and build a huge graph for every module
print("Please disconnect network and press any key.")
input()

# For each ontology except full,:
for inputFile in ontologyFiles:
    if not inputFile.startswith("full"):
        # 1. Generate PyLODE docs
        fEnding = splitext(inputFile)[1]
        outputFileName = inputFile.replace(fEnding, ".html")
        subprocess.run([pylodePath, "-i", f"{ontologyPath}/{inputFile}", "-o", f"{ontologyPath}/{outputFileName}"])

        # 2. Merge into temp full graph
        moduleGraph = Graph()
        moduleGraph.parse(f"{ontologyPath}/{inputFile}")
        moduleOntologyUris = list(moduleGraph.subjects(RDF.type, OWL.Ontology))
        for (s, p, o) in moduleGraph:
            if not s in moduleOntologyUris:
                unionedOntology.add((s, p, o))

        # 3. Generate WebVOWL visualization (except for metadata file)
        if not inputFile.startswith("metadata"):
            outputJsonFileName = outputFileName.replace(".html",".json")
            subprocess.run(["java", "-jar", owl2vowlPath, "-file", f"{ontologyPath}/{inputFile}", "-output", f"{ontologyPath}/webvowl/data/{outputJsonFileName}"])

print("Please reconnect network and press any key.")
input()

# 4. Export unioned full ontology to temp file, run pylode, kill temp file
unionedOntology.serialize(destination=f"{ontologyPath}/fullTemp.ttl", format="turtle")
subprocess.run([pylodePath, "-i", f"{ontologyPath}/fullTemp.ttl", "-o", f"{ontologyPath}/full.html"])
remove(f"{ontologyPath}/fullTemp.ttl")

# 5. Generate WebVOWL visualization on full file
subprocess.run(["java", "-jar", owl2vowlPath, "-file", f"{ontologyPath}/full.rdf", "-output", f"{ontologyPath}/webvowl/data/full.json"])

# 6. Graft on HTML <iframe>s
# TODO