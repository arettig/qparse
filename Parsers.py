import numpy as np
import re



def fatal(jobText):
    linePattern = re.compile(r"fatal")
    matches = re.findall(linePattern, jobText)
    return matches != []
    
def dist(jobText, atom1, atom2):
    floatPattern = "-*[0-9]+\.*[0-9]*"
    distPattern1 = re.compile(atom1 + "\s+" + floatPattern + "\s+" + floatPattern + "\s+" + floatPattern)
    distPattern2 = re.compile(atom2 + "\s+" + floatPattern + "\s+" + floatPattern + "\s+" + floatPattern)

    distMatch1 = re.findall(distPattern1, jobText)
    distMatch2 = re.findall(distPattern2, jobText)

    if(len(distMatch1) == 0 and len(distMatch2) == 0):
        return None
    elif(len(distMatch1) == 0 or (atom1 == atom2 and len(distMatch1) == 1)):
        return float(distMatch2[0].split()[2])
    elif(len(distMatch2) == 0):
        return float(distMatch1[0].split()[2])
    else:
        ind2 = 0
        if(atom1 == atom2):
            ind2 = 1
        return abs(float(distMatch2[ind2].split()[-1]) - float(distMatch1[0].split()[-1]))


def GSEnergy(jobText):
    linePattern = re.compile(r"Total energy in.*")
    matches = re.findall(linePattern, jobText)
    if(matches == []):
        return None
    else:
        return float(matches[0].split()[-1])


def GSSpin(jobText):
    linePattern = re.compile(r"S\^2.*")
    matches = re.findall(linePattern, jobText)
    if(matches == []):
        return None
    else:
        return float(matches[0].split()[-1])

    
def CISEnergies(jobText):
    jobText = trimCIS(jobText)    
    linePattern = re.compile(r"Total energy for state.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-2]) for x in matches][NRoots(jobText)]

    
def CISSpins(jobText):
    jobText = trimCIS(jobText)
    linePattern = re.compile(r"S\*\*2.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-1]) for x in matches][NRoots(jobText)]


def CISDEnergies(jobText):
    jobText = trimCISD(jobText)    
    linePattern = re.compile(r"Total energy for state.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-2]) for x in matches][NRoots(jobText)]


def CISDTerm1(jobText):
    linePattern = re.compile(r"term1.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-1]) for x in matches][NRoots(jobText)]

    
def CISDTerm2(jobText):
    linePattern = re.compile(r"term2.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-1]) for x in matches][NRoots(jobText)]







# helpers

def trimCIS(jobText):
    startInd = jobText.find("CIS Excitation Energies")
    endInd = jobText[startInd+90:].find("---------------")
    return jobText[startInd:endInd]


def trimCISD(jobText):
    startInd = jobText.find("RI-CIS(D) Excitation Energies")
    endInd = jobText[startInd+93:].find("---------------")
    return jobText[startInd:endInd]


def NStates(jobText):
    rootsLine = re.findall("cis_n_roots.*",jobText)
    rootsLine += re.findall("EE_STATES .*", jobText)
    if(len(rootsLine) == 0):
        singletsLine = re.findall("EE_SINGLETS .*", jobText)
        tripletsLine = re.findall("EE_TRIPLETS .*", jobText)
        if(len(singletsLine) + len(tripletsLine) == 0):
            return None
        else:
            nroots = int(singletsLine[0].split()[-1]) + int(tripletsLine[0].split()[-1])
    else:
        nroots = int(rootsLine[0].split()[-1])
    
    return nroots

