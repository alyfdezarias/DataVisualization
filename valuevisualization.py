#data visualization
#objective value
from cProfile import label
import math
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from sympy import true

class ItemData:
    def __init__(self, best, second, rest, label):
        self.best = best
        self.second = second
        self.rest = rest
        self.label = label

    def __str__(self):
        return f"Best={self.best}, Second={self.second}, Rest={self.rest}"

    def totaltest(self):
        return self.best+self.second+self.rest

def create_parser():
    parser = argparse.ArgumentParser(prog = "valuevisualization")
    parser.add_argument("-d", "--datafile", type = str, default = "data1.csv")
    return parser

def load_algorithms_performace(customFrame, countNAN=True):
    performance = {
        'BandC':ItemData(0,0,0, "Branch and Cut"),
        'FandR11':ItemData(0,0,0, "Fixed and Relax\n"+r"$\alpha=1, \beta=1$"), 
        'FandR23':ItemData(0,0,0, "Fixed and Relax\n"+r"$\alpha=2, \beta=3$")
        }
    for index, row in customFrame.iterrows():
        custom = {
            "BandC":row['Branch_and_Cut_Objective_Value'],
            "FandR11":row['Fixed_and_Relax_alpha1beta1_Objective_Value'],
            "FandR23":row['Fixed_and_Relax_alpha2beta3_Objective_Value']
            }
        for k,v in custom.items():
            if math.isnan(v):
                custom[k] = math.inf
        minvalue = min(custom.values())
        diff = {}
        for k,v in custom.items():
            diff[k] = v-minvalue
            if diff[k] == 0:
                performance[k].best += 1
            elif diff[k] <= 0.5*minvalue:
                performance[k].second += 1
            elif countNAN or not math.isinf(diff[k]):
                performance[k].rest +=1
    return performance

def plot_performance(performanceData, horizontal=True):
    best = [v.best for v in performanceData.values()]
    second = [v.second for v in performanceData.values()]
    rest = [v.rest for v in performanceData.values()]

    plt.clf()
    ind = [v.label for v in performanceData.values()]
    restbnt = [x+y for x,y in zip(best, second)]
    if horizontal:
        plt.bar(ind, best, color=["#b32d00", "#000099", "#0d5409"], edgecolor='white', align='center')
        plt.bar(ind, second, bottom=best, color=["#ff531a", "#0000ff", "#398e34"], hatch="/", edgecolor='white', align='center')
        plt.bar(ind, rest, bottom=restbnt, color=["#ffc6b3","#b3b3ff", "#9dd99a"], edgecolor='white', align='center')
        plt.ylabel("Number of Instances Solved")
    else:
        plt.barh(ind, best, color=["#b32d00", "#000099", "#0d5409"], edgecolor='white', align='center')
        plt.barh(ind, second, left=best, color=["#ff531a", "#0000ff", "#398e34"], hatch="/", edgecolor='white', align='center')
        plt.barh(ind, rest, left=restbnt, color=["#ffc6b3","#b3b3ff", "#9dd99a"], edgecolor='white', align='center')
        plt.xlabel("Number of Instances Solved")

    #plt.xticks([])
    # colors = {'Branch and Cut':'#b32d00', r'Fixed and Relax $\alpha=1, \beta=1$':'#000099', r'Fixed and Relax $\alpha=2, \beta=3$':"#0d5409"}         
    # labels = list(colors.keys())
    # handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    #plt.legend(handles, labels)
    #plt.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.01), fancybox=True, shadow=True, ncol=2)
    plt.tight_layout()
    plt.show()



def main():
    parser = create_parser()
    args = parser.parse_args()

    # value performance
    #mydata = pd.read_csv(args.datafile, usecols=['Instance','Branch_and_Cut_Objective_Value', 'Status_obj', 'Fixed_and_Relax_alpha1beta1_Objective_Value', 'Fixed_and_Relax_alpha2beta3_Objective_Value'])
    mydata = pd.read_csv(args.datafile, usecols=['Branch_and_Cut_Objective_Value', 'Fixed_and_Relax_alpha1beta1_Objective_Value', 'Fixed_and_Relax_alpha2beta3_Objective_Value'])
    myframe = pd.DataFrame(mydata)
    performance = load_algorithms_performace(myframe, True)
    plot_performance(performance, horizontal=True)
    plot_performance(performance, horizontal=False)
    performance = load_algorithms_performace(myframe, False)
    plot_performance(performance, horizontal=True)
    plot_performance(performance, horizontal=False)


    
if __name__ == "__main__":
    main()

