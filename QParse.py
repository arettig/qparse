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
    GS = True
    CIS = False
    CISD = False

    # private vars
    infile = None
    mFile = None
    jobStart = 0
    jobEnd = -1

    dists = []
    GSEnergies = []
    GSSpins = []
    CISEnergies = []
    CISSpins = []
    CISDEnergies = []
    CISDTerm1s = []
    CISDTerm2s = []

    def __init__(self, files):
        fileNames = files
        
    def parse():
        # loop through files
        for f in fileNames:
            jobStart = 0
            jobEnd = 0
            mFile = None
            
            parseFile(f)

            
    def parseFile(filename):
        # loop through jobs in file
        doneWithFile = False

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
        if(GS):
            GSEnergies.append(prs.GSEnergy(jobText))
            GSSpins.append(prs.GSSpin(jobText))
        if(CIS):
            CISEnergies.append(prs.CISEnergies(jobText))
            CISSpins.append(prs.CISSpin(jobText))
        if(CISD):
            CISDEnergies.append(prs.CISDEnergies(jobText))
            CISDTerm1s.append(prs.term1(jobText))
            CISDTerm2s.append(prs.term2(jobText))


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
