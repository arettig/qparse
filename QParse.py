import numpy as np
import mmap
import Parsers as prs


jobMatchPattern = "Thank you very much"
jobMatchOffset = len(jobMatchPattern)


class QParser:
    # public vars
    fileNames = []

    dist = True
    atom1 = "H"
    atom2 = "H"
    GSEnergy = True
    ESEnergy = False
    GSSpin = True
    ESSpin = False

    # private vars
    infile = None
    mFile = None
    jobStart = 0
    jobEnd = -1

    dists = []
    GSEnergies = []
    ESEnergies = []
    GSSpins = []
    ESSpins = []

    def __init__(self, files):
        fileNames = files
        
    def parse():
        # loop through files
        for f in fileNames:
            jobStart = 0
            jobEnd = 0
            mFile = None
            
            # loop through jobs in file
            doneWithFile = False
                    

    def parseFile(filename):
        while(not doneWithFile):
            jobText, doneWithFile = getNextJobText(filename)

            # check for crash
            if(prs.fatal(jobText)):
                continue

            parseJob(jobText)

            
    def parseJob(jobText):
        # parse out requested values
        if(dist):
            dists.append(prs.dist(jobText, atom1, atom2))
        if(GSEnergy):
            GSEnergies.append(prs.GSEnergy(jobText))
        if(ESEnergy):
            ESEnergies.append(prs.ESEnergies(jobText))
        if(GSSpin):
            GSSpins.append(prs.GSSpin(jobText))
        if(ESSpin):
            ESSpins.append(prs.ESSpin(jobText))

            
    def getNextJobText(fileName):
        # mmap file
        if(mFile == None):
            infile = open(fileName, 'r')
            mFile = mmap.mmap(inFile.fileno(), 0, prot=mmap.PROT_READ)

        # read next job into memory
        mFile.seek(jobStart)
        jobEnd = mFile.find(jobMatchPattern)
        if(jobEnd == -1):
            jobEnd = mFile.size()
        jobText = mFile.read(jobEnd - jobStart)

        #move buffer pointer to start of next job:
        jobStart = jobEnd + jobMatchOffset

        return jobText, jobEnd == mFile.size()
