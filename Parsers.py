import numpy as np
import re



def fatal(jobText, args):
    linePattern = re.compile(b"fatal")
    matches = re.findall(linePattern, jobText)
    return matches != []
    
def dist(jobText, args):
    atom1 = args[0]
    atom2 = args[1]
    
    jobText = trimGeom(jobText)
    floatPattern = b"-*[0-9]+\.*[0-9]*"
    distPattern1 = re.compile(atom1.encode() + b"\s+" + floatPattern + b"\s+" + floatPattern + b"\s+" + floatPattern)
    distPattern2 = re.compile(atom2.encode() + b"\s+" + floatPattern + b"\s+" + floatPattern + b"\s+" + floatPattern)

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


def GSEnergy(jobText, args):
    linePattern = re.compile(b"Total energy in.*")
    matches = re.findall(linePattern, jobText)
    if(matches == []):
        return None
    else:
        return float(matches[0].split()[-1])
    

def GSSpin(jobText, args):
    linePattern = re.compile(b"S\^2.*")
    matches = re.findall(linePattern, jobText)
    if(matches == []):
        return None
    else:
        return float(matches[0].split()[-1])

    
def CISEnergies(jobText, args):
    nroots = NRoots(jobText)
    jobText = trimCIS(jobText)    
    linePattern = re.compile(b"Total energy for state.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-2]) for x in matches][:nroots]

    
def CISSpins(jobText, args):
    nroots = NRoots(jobText)
    jobText = trimCIS(jobText)
    linePattern = re.compile(b"S\*\*2.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-1]) for x in matches][:nroots]

def CISDGSEnergy(jobText, args):
    linePattern = re.compile(b"RIMP2         total energy.*")
    matches = re.findall(linePattern, jobText)
    if(matches == []):
        return None
    else:
        return float(matches[0].split()[-2])

def CISDEnergies(jobText, args):
    nroots = NRoots(jobText)
    jobText = trimCISD(jobText)
    linePattern = re.compile(b"Total energy for state.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-2]) for x in matches][:nroots]


def CISDTerm1(jobText, args):
    nroots = NRoots(jobText)
    linePattern = re.compile(b"term1.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-2]) for x in matches][:nroots]

    
def CISDTerm2(jobText, args):
    nroots = NRoots(jobText)
    linePattern = re.compile(b"term2.*")
    matches = re.findall(linePattern, jobText)

    if(matches == []):
        return None
    else:
        return [float(x.split()[-2]) for x in matches][:nroots]


def CCSDpTEnergy(jobText, args):
    linePattern = re.compile(b"CCSD\(T\) total.*")
    matches = re.findall(linePattern, jobText)
    if(matches != []):
        return float(matches[0].split()[-1])


def CCSDEnergy(jobText, args):
    linePattern = re.compile(b"CCSD total.*")
    matches = re.findall(linePattern, jobText)
    if(matches != []):
        return float(matches[0].split()[-1])


def CC2Energy(jobText, args):
    matches = re.findall(b"CC2 total energy.*", jobText)
    if(matches != []):
        return float(matches[0].split()[-1])

def SCFEnergy(jobText, args):
    matches = re.findall(b"SCF energy.*", jobText)
    if(matches != []):
        return float(matches[0].split()[-1])

def MP2Energy(jobText, args):    
    matches = re.findall(b"MP2         total energy.*", jobText)
    if(matches != []):
        return float(matches[0].split()[-2])

    matches = re.findall(b"MP2 energy.*", jobText)
    if(matches != []):
        return float(matches[0].split()[-1])
    
def koomp2CorrEnergy(jobText, args):
    matches = re.findall(b"RIMP2   correlation energy.*", jobText)
    if(matches != []):
        return float(matches[-1].split()[-2])

def MP3Energy(jobText, args):
    matches = re.findall(b"MP3 energy .*", jobText)
    if(matches != []):
        return float(matches[-1].split()[-1])

def EEEnergy(jobText, args):
    matches = re.findall(b"Excitation energy.*", jobText)
    if(matches != []):
        return [float(m.split()[-2]) for m in matches]

def Transitions(jobText, args):
    pattern = re.compile("Amplitude    Transitions between orbitals.*\n(?:.*->.*\n)*.*\n.*Summary", re.MULTILINE)
    matches = re.findall(pattern, jobText)
    matches = [m.split("\n")[1:-2] for m in matches]

    vecs = []
    for m in matches:
        vecs.append(getTransVec(m))

    return np.array(vecs).T

def BCC2Energy(jobText, args):
    pattern = re.compile(b"CC2 ENERGY.*")
    matches = re.findall(pattern, jobText)
    if(matches != []):
        finalEnergy = float(matches[-1].split()[-1])
        return finalEnergy

def kMP2Energy(jobText, args):
    pattern = re.compile(b"RIMP2         total energy.*")
    match = re.search(pattern, jobText)
    if(match != None):
        return float(match.group(0).split()[-2])

def TAmps(jobText, args):
    pattern = re.compile(b"t amps.*\n((?:\s|[0-9]|\.|-|\+|\n|e)*)", re.MULTILINE)
    matches = re.findall(pattern, jobText)

    ts = []
    for match in matches:
        lineSplitMatches = match.split(b"\n")
        for line in lineSplitMatches:
            vals = [float(t) for t in line.split()]
            ts += vals

    return np.array(ts)


def MP2NBS(jobText, args):    
    matches = re.findall(b"non-Brillouin singles    =.*", jobText)
    if(matches != []):
        return float(matches[0].split()[-2])

def integMag(jobText, args):
    matches = re.findall(b"Integral magnitude.*", jobText)
    if(matches != []):
        return float(matches[-1].split()[-1])
#
# helpers
#

def trimGeom(jobText):
    startInd = jobText.find(b"$molecule")
    endInd = jobText.find(b"$end")
    return jobText[startInd:endInd]


def trimCIS(jobText, args):
    startInd = jobText.find(b"CIS Excitation Energies")
    endInd = jobText[startInd+90:].find("---------------") + startInd + 90
    return jobText[startInd:endInd]


def trimCISD(jobText, args):
    startInd = jobText.find(b"RI-CIS(D) Excitation Energies")
    endInd = jobText[startInd+93:].find("---------------") + startInd + 93
    return jobText[startInd:endInd]


def NRoots(jobText, args):
    rootsLine = re.findall(b"cis_n_roots.*",jobText)
    rootsLine += re.findall(b"EE_STATES .*", jobText)
    if(len(rootsLine) == 0):
        singletsLine = re.findall(b"EE_SINGLETS .*", jobText)
        tripletsLine = re.findall(b"EE_TRIPLETS .*", jobText)
        if(len(singletsLine) + len(tripletsLine) == 0):
            return None
        else:
            nroots = int(singletsLine[0].split()[-1]) + int(tripletsLine[0].split()[-1])
    else:
        nroots = int(rootsLine[0].split()[-1])
    
    return nroots

def getTransVec(transitions):
    l = 300
    vec = np.zeros(l)
    for t in transitions:
        vals = t.split()
        amp = float(vals[0])
        from_ind = int(vals[1]) + (l/4 if vals[3] == "A" else 0)
        to_ind = l/2 + int(vals[5]) + (l/4 if vals[3] == "A" else 0)
        vec[from_ind] -= amp
        vec[to_ind] += amp
    return vec
        
