#!/usr/bin/env python3

import sys
import subprocess
from os import listdir, remove, rename
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
        inputFilePath = f"{ontologyPath}/{inputFile}"
        # 1. Generate PyLODE docs
        moduleName, fEnding = splitext(inputFile)
        outputHtmlFileName = f"{ontologyPath}/{moduleName}.html"
        subprocess.run([pylodePath, "-i", inputFilePath, "-o", outputHtmlFileName])

        # 2. Merge into temp full graph
        moduleGraph = Graph()
        moduleGraph.parse(inputFilePath)
        moduleOntologyUris = list(moduleGraph.subjects(RDF.type, OWL.Ontology))
        for (s, p, o) in moduleGraph:
            if not s in moduleOntologyUris:
                unionedOntology.add((s, p, o))

        # 3. Generate and graft WebVOWL visualization (except for metadata file)
        if not inputFile.startswith("metadata"):
            outputJsonFilePath = f"{ontologyPath}/webvowl/data/{moduleName}.json"
            subprocess.run(["java", "-jar", owl2vowlPath, "-file", inputFilePath, "-output", outputJsonFilePath])

            # Graft on HTML <iframe>s
            htmlFile = open(outputHtmlFileName, "rt")
            htmlContent = htmlFile.read()
            htmlFile.close()
            htmlContent = htmlContent.replace('<div style="width:500px; height:50px; background-color: black;">&nbsp;</div>', f'<iframe src="webvowl/index.html#{moduleName}" width="100%" height="800"></iframe>')
            htmlFile = open(outputHtmlFileName, "wt")
            htmlFile.write(htmlContent)
            htmlFile.close()

print("Please reconnect network and press any key.")
input()

# 4. Export unioned full ontology to temp file, run pylode, kill temp file
rename(f"{ontologyPath}/full.rdf", f"{ontologyPath}/fullTemp.rdf")
unionedOntology.serialize(destination=f"{ontologyPath}/full.rdf", format="rdfxml")
subprocess.run([pylodePath, "-i", f"{ontologyPath}/full.rdf", "-o", f"{ontologyPath}/full.html"])
remove(f"{ontologyPath}/full.rdf")
rename(f"{ontologyPath}/fullTemp.rdf", f"{ontologyPath}/full.rdf")

# 5. Generate WebVOWL visualization on full file and graft it
subprocess.run(["java", "-jar", owl2vowlPath, "-file", f"{ontologyPath}/full.rdf", "-output", f"{ontologyPath}/webvowl/data/full.json"])
htmlFile = open(f"{ontologyPath}/full.html", "rt")
htmlContent = htmlFile.read()
htmlFile.close()
htmlContent = htmlContent.replace('<div style="width:500px; height:50px; background-color: black;">&nbsp;</div>', f'<iframe src="webvowl/index.html#full" width="100%" height="800"></iframe>')
htmlFile = open(f"{ontologyPath}/full.html", "wt")
htmlFile.write(htmlContent)
htmlFile.close()