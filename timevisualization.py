#data visualization
#time performance
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import math

class VersionData:
    def __init__(self, version, BandC, FandR11, FandR23):
        self.version = version
        self.BandC = BandC
        self.FandR11 = FandR11
        self.FandR23 = FandR23
        

class ItemData:
    def __init__(self, testcase):
        self.testcase =  testcase
        self.versionlist = []

    def add(self, version, BandC, FandR11, FandR23):
        self.versionlist.append(VersionData(version, BandC, FandR11, FandR23))

    def get_BandC_times(self):
        return [v.BandC for v in self.versionlist if not math.isnan(v.BandC) ]
    
    def get_FandR11_times(self):
        return [v.FandR11 for v in self.versionlist if not math.isnan(v.FandR11)]

    def get_FandR23_times(self):
        return [v.FandR23 for v in self.versionlist if not math.isnan(v.FandR23)]

    
def create_parser():
    parser = argparse.ArgumentParser(prog = "timevisualization")
    parser.add_argument("-d", "--datafile", type = str, default = "data1.csv")
    return parser

def load_algorith_time_performance(customFrame):
    performance = {}
    for index, row in customFrame.iterrows():
        testcaseinfo = row['Instance'].split('_ver')
        testcase = testcaseinfo[0]
        version = int(testcaseinfo[1])
        BandC = row['Branch_and_Cut_CPU_time']
        FandR11 = row['Fixed_and_Relax_alpha1beta1_CPU_time']
        FandR23 = row['Fixed_and_Relax_alpha2beta3_CPU_time']
        if not testcase in performance:
            performance[testcase] = ItemData(testcase)
        performance[testcase].add(version, BandC, FandR11, FandR23)
    return performance
        
def plot_time_performance(performanceData):
    plt.clf()
    testid = range(1, len(performanceData)+1)
    testnames = [k for k in performanceData.keys()]
    BandC_mean = [sum(i.get_BandC_times())/len(i.get_BandC_times()) for i in performanceData.values()]
    BandC_min = [min(i.get_BandC_times()) for i in performanceData.values()]
    BandC_max = [max(i.get_BandC_times()) for i in performanceData.values()]
    plt.plot(testid, BandC_mean, "o-", color="#b32d00", label="Branch and Cut")
    plt.fill_between(testid, BandC_min, BandC_max, alpha=0.2)
    FandR11_mean = [sum(i.get_FandR11_times())/len(i.get_FandR11_times()) for i in performanceData.values()]
    FandR11_min = [min(i.get_FandR11_times()) for i in performanceData.values()]
    FandR11_max = [max(i.get_FandR11_times()) for i in performanceData.values()]
    plt.plot(testid, FandR11_mean, "o-", color="#000099", label="Fixed and Relax "+r"$\alpha=1, \beta=1$")
    plt.fill_between(testid, FandR11_min, FandR11_max, alpha=0.2)
    FandR23_mean = [sum(i.get_FandR23_times())/len(i.get_FandR23_times()) for i in performanceData.values()]
    FandR23_min = [min(i.get_FandR23_times()) for i in performanceData.values()]
    FandR23_max = [max(i.get_FandR23_times()) for i in performanceData.values()]
    plt.plot(testid, FandR23_mean, "o-", color="#0d5409", label="Fixed and Relax "+r"$\alpha=2, \beta=3$")
    plt.fill_between(testid, FandR23_min, FandR23_max, alpha=0.2)
    plt.legend()
    plt.xticks(testid, testnames, rotation='vertical')
    plt.tight_layout()
    plt.show()


def main():
    parser = create_parser()
    args = parser.parse_args()

    #time performance
    mydata = pd.read_csv(args.datafile, usecols=['Instance', 'Status_obj', 'Branch_and_Cut_CPU_time', 'Fixed_and_Relax_alpha1beta1_CPU_time', 'Fixed_and_Relax_alpha2beta3_CPU_time'])
    myframe = pd.DataFrame(mydata)
    performance = load_algorith_time_performance(myframe)
    plot_time_performance(performance)

    





    
if __name__ == "__main__":
    main()