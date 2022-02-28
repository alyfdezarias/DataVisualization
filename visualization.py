from cProfile import label
from cmath import nan
from doctest import testfile
import math
import random
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import false


class ItemData:
    def __init__(self, best, second, rest):
        self.best = best
        self.second = second
        self.rest = rest

def create_parser():
    parser = argparse.ArgumentParser(prog = "visualization")
    parser.add_argument("-d", "--datafile", type = str, default = "data.csv")
    return parser

def get_multivals(myframe, colName):
    minVal = []
    maxVal = []
    centralVal = []
    testFile = []
    for index, row in myframe.iterrows():
        customval = row[colName]
        testFile.append(row['Instance'])
        if not math.isnan(customval):      
            minVal.append(customval*random.random())
            centralVal.append(customval)
            maxVal.append(customval*(1+random.random()))
        else:
            minVal.append(nan)
            centralVal.append(nan)
            maxVal.append(nan)
    return testFile, minVal, maxVal, centralVal


def main():
    parser = create_parser()
    args = parser.parse_args()

    mydata = pd.read_csv(args.datafile, usecols=['Instance','BandCval', 'FandRval'])
    myframe = pd.DataFrame(mydata, columns=['BandCval', 'FandRval'])

    vdata = {'BandC':ItemData(0,0,0), 'FandR':ItemData(0,0,0)}
    for index, row in myframe.iterrows():
        BandC = row['BandCval']
        FandR = row['FandRval']
        if not math.isnan(BandC) and not math.isnan(FandR):
            diff = BandC - FandR
            if diff == 0:
                vdata['BandC'].best += 1
                vdata['FandR'].best += 1
            elif diff < 0: #best is BandC
                vdata['BandC'].best += 1
                if abs(diff) <= 0.05*BandC: #gap FandR is less than 5%
                    vdata['FandR'].second += 1
                else: 
                    vdata['FandR'].rest += 1
            else:#best is FandR
                if abs(diff) <= 0.05*FandR: #gap BandC is less than 5%
                    vdata['BandC'].second += 1
                else:
                    vdata['BandC'].rest += 1
                    #print(f"rest BandC")
        elif not math.isnan(BandC):
            vdata['BandC'].best += 1
        elif not math.isnan(FandR):
            vdata['FandR'].best += 1

    for k,v in vdata.items():
        print(f"{k}.best={v.best}, .second={v.second} .rest={v.rest}")


    best = [vdata["BandC"].best, vdata["FandR"].best]
    second = [vdata["BandC"].second, vdata["FandR"].second]
    rest = [vdata["BandC"].rest, vdata["FandR"].rest]
   
    print(f"performance of the algorithms")
    plt.clf()
    ind = ["BandC", "FandR"]
    restbnt = [x+y for x,y in zip(best, second)]
    plt.bar(ind, best, color=["#b32d00", "#000099"], edgecolor='white', align='center', width=0.3)
    plt.bar(ind, second, bottom=best, color=["#ff531a", "#0000ff"], hatch="/", edgecolor='white', align='center', width=0.3)
    plt.bar(ind, rest, bottom=restbnt, color=["#ffc6b3","#b3b3ff"], edgecolor='white', align='center', width=0.3)
    plt.xticks([])
    colors = {'Branch and Cut':'#b32d00', 'Fixed and Relax':'#000099'}         
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.legend(handles, labels)
    plt.show()

    print(f"performance of the instances")
    testFile = []
    BandCmin = []
    BandCmax = []
    BandCval = []
    FandRmin = []
    FandRmax = []
    FandRval = []
    myframe = pd.DataFrame(mydata, columns=['Instance', 'BandCval', 'FandRval'])
    testFile, BandCmin, BandCmax, BandCval = get_multivals(myframe, 'BandCval')
    testFile, FandRmin, FandRmax, FandRval = get_multivals(myframe, 'FandRval')
    
    xvals = np.arange(len(testFile))
    plt.plot(xvals, BandCval, "o-", color="b", label="Branch and Cut")
    plt.fill_between(xvals, BandCmin, BandCmax, alpha=0.2)
    plt.plot(xvals, FandRval, "o-", color="r", label="Fixed and Relax")
    plt.fill_between(xvals, FandRmin, FandRmax, alpha=0.2)
    plt.xticks(xvals, testFile, rotation='vertical')
    plt.legend()
    plt.tight_layout()
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()







        
    






if __name__ == "__main__":
    main()