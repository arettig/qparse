import numpy as np
import mmap
import Parsers as prs


JOB_MATCH_PATTERN = "Welcome to Q-Chem"
JOB_PATTERN_OFFSET = len(JOB_MATCH_PATTERN)


class QParser:
    verbose = False
    
    def __init__(self, verbose = False):
        self.verbose = verbose
            
    def parseFile(self, filename, parseMethod, args = []):
        infile = open(filename, 'r')
        mFile = mmap.mmap(infile.fileno(), 0, prot=mmap.PROT_READ)
        jobStart = mFile.find(JOB_MATCH_PATTERN.encode("utf-8")) + JOB_PATTERN_OFFSET
        jobEnd = -1
        doneWithFile = False
        
        if(self.verbose):
            print("Processing " + filename)

        vals = []

        # loop through jobs in file
        while(not doneWithFile):
            jobText, doneWithFile, jobStart, jobEnd = self.getNextJobText(mFile, jobStart, jobEnd)

            # check for crash
            #if(prs.fatal(jobText, args)):
             #   continue

            vals.append(parseMethod(jobText, args))

        infile.close()
        return vals

    def getNextJobText(self, mFile, jobStart, jobEnd):
        # read next job into memory
        mFile.seek(jobStart)
        jobEnd = mFile.find(JOB_MATCH_PATTERN.encode("utf-8"))
        if(jobEnd == -1):
            jobEnd = mFile.size()
        jobText = mFile.read(jobEnd - jobStart)

        #move buffer pointer to start of next job:
        jobStart = jobEnd + JOB_PATTERN_OFFSET + 200

        return jobText, jobStart >= mFile.size(), jobStart, jobEnd

    def dists(self, infile, atom1, atom2):
        return self.parseFile(infile, prs.dist, args=[atom1, atom2])

    def GSEnergies(self, infile):
        return self.parseFile(infile, prs.GSEnergy)

    def GSSpins(self, infile):
        return self.parseFile(infile, prs.GSSpin)
    
    def CISEnergies(self, infile):
        return self.parseFile(infile, prs.CISEnergies)

    def CISSpins(self, infile):
        return self.parseFile(infile, prs.CISSpins)

    def MP2Energies(self, infile):
        return self.parseFile(infile, prs.MP2Energy)

    def CISDEnergies(self, infile):
        return self.parseFile(infile, prs.CISDEnergies)

    def CCSDpTEnergies(self, infile):
        return self.parseFile(infile, prs.CCSDpTEnergy)

    def CCSDEnergies(self, infile):
        return self.parseFile(infile, prs.CCSDEnergy)

    def CC2Energies(self, infile):
        return self.parseFile(infile, prs.CC2Energy)

    def MP3Energies(self, infile):
        return self.parseFile(infile, prs.MP3Energy)

    def SCFEnergies(self, infile):
        return self.parseFile(infile, prs.SCFEnergy)

    def EEEnergies(self, infile):
        return self.parseFile(infile, prs.EEEnergy)
    
    def Transitions(self, infile):
        return self.parseFile(infile, prs.Transitions)

    def BCC2Energies(self, infile):
        return self.parseFile(infile, prs.BCC2Energy)

    def kMP2Energies(self, infile):
        return self.parseFile(infile, prs.kMP2Energy)

    def TAmplitudes(self, infile):
        return self.parseFile(infile, prs.TAmps)

    def MP2NBS(self, infile):
        return self.parseFile(infile, prs.MP2NBS)

    def integMags(self, infile):
        return self.parseFile(infile, prs.integMag)
    
