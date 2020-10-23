#!/usr/bin/env python3

import sys, getopt

def getEnvString(envFilename):
    envString = ""
    try:
        envFile = open(envFilename, "r");
    except IOError:
        print("Error: " + envFilename + " not found.")
        sys.exit(2)

    envLines = envFile.readlines();
    
    envFile.close()

    for line in envLines:
        envString += line.rstrip().replace("'", "\"") + ","
    envString = envString[:-1]

    return envString

def injectEnvStringInOutput(envString, outFilename):
    try:
        outFile = open(outFilename, "r")
    except IOError:
        print("Error: " + outFilename + " not found.")
        sys.exit(2)

    outLines = outFile.readlines()
    outFile.close()
    outFile = open(outFilename, "w")
    for line in outLines:
        print(line)
        if line.startswith("environment"):
            line = "environment = " + envString + "\n"
        outFile.write(line)
    outFile.close()
    print("All Env variable has been written in " + outFilename + ".")
    
def main(argv):
    inputEnvFile = ''
    outputFile = ''

    try:
        opts, args = getopt.getopt(argv[1:], "he:o:", ["envfile=", "outputfile="])
    except getopt.GetoptError:
        print(argv[0] + ' -e <envfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(argv[0] + ' -e <envfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-e", "--envfile"):
            inputEnvFile = arg
        elif opt in ("-o", "--outputfile"):
            outputFile = arg
    
    envString = getEnvString(inputEnvFile)
    if outputFile == '':
        print(envString)
    else:
        injectEnvStringInOutput(envString, outputFile)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(sys.argv[0] + " -h to display needed arguments.")
        sys.exit(1)
    else:
        main(sys.argv)
    sys.exit()
