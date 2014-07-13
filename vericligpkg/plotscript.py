'''
Created on Jun 17, 2013

@author: camilothorne
'''


from __future__ import division
import array
from matplotlib import pylab, cm
from numpy import *
from operator import itemgetter, attrgetter
import scipy
from time import time

# statistical test(s)
from corpuspkg.statstests import *


# Class encoding the plot
class ExpPlotB:
     
     
    #constructor
    def __init__(self):
        mys = MMStats()
        statsA = mys.expOne
        statsB = mys.expTwo
        statsC = mys.expThree 
        fig = pylab.figure(figsize=(8,8), dpi=100)      
        self.plotPer(fig,statsA,2,len(statsA),"Context",('avg.','NP','Sen'),1)     
        self.plotPer(fig,statsB,6,len(statsB),"Features",('avg.','avg. (all)',
                                                            'Logit','SVM','Bayes','Neural','Tree','kNN'),2)
        self.plotPer(fig,statsC,4,len(statsC),"Features2",('avg.','avg. (all)',
                                                            'Logit','Bayes','Neural','Tree'),3)
        pylab.ioff()
        mys.tests()
        #to use if needed
        mytime = '%.2f' % time()
        #mytime = ""
        #fig.savefig('/home/camilo/Desktop/'+name+'-vericlig'+mytime+'.eps') 
        #fig.savefig('/home/camilo/Desktop/experiments-vericlig'+mytime+'.pdf')
        fig.subplots_adjust(left=0.2, bottom=None, right=None, top=None, wspace=0.8, hspace=0.4)
        #fig.suptitle("Feature selection experiments"+"\n\n", fontsize=14) 
        pylab.show()      
        
                            
    # bar chart + plotter component    
    def plotPer(self,figu,stats,f_num,c_num,name,li,pos):
        ax = figu.add_subplot(2,2,pos)
        ind = pylab.arange(c_num)
        width = 1
        i = 0
        max = 1
        ctags = stats.keys()
        mytags = []
        # plot bars
        self.barPlot3(ax,ind,width,f_num,ctags,stats,i)
        if name == "Context":
            # means
            means = self.defineAvg(stats,f_num,c_num)
            # plot means
            ax.plot((ind+width/2),means,'o-',# change line type
                color='k',linewidth=3,label="average") # change color
        else:
            means = self.defineAvg(stats,f_num,c_num)
            base = []
            for i in range(c_num):
                
                #base.append(0.69) # activity Tree precision
                #base.append(0.66) # temporal rel. Tree precision             
                base.append(0.59) # activity avg precision
                #base.append(0.51) # temporal rel. avg precision                
                              
            # plot means
            ax.plot((ind+width/2),means,'o-',# change line type
                color='k',linewidth=3,label="average") # change color
            # plot base
            ax.plot((ind+width/2),base,'x-',# change line type
                color=`0.50`,label="base") # change color
        # plot labels        
        ax.set_title(name+'\n\n',
                     fontstyle='normal',fontsize='9')
        # setting axis
        ax.axis([0,c_num,0,max])
        ax.set_ylabel("precision",fontsize='9')
        # plot class names
        for c in range(c_num):
            mytags.append(c+(width/2))
        ax.set_xticks(mytags)
        ax.set_xticklabels(ctags,rotation='45',fontsize='9')
        ax.grid(False)
        # plot legend
        self.plotLegend(ax,li)
     
            
    # plotting the bars in the chart
    def barPlot3(self,ax,ind,width,f_num,ctags,stats,i):
        cstats = []
        for i in range(f_num):
            cstats.append([])
        for i in range(f_num):
            for id in stats.keys():
                cstats[i].append(stats[id][i])
        for i in range(f_num):
            if f_num == 2:     
                flo = 0.75/(i+1)
            else:
                flo = 0.95-(i/8)
            bars = ax.bar(ind,cstats[i],width/f_num,color=""+`flo`+"",linewidth=1,edgecolor='k')
            for rect in bars:
                rect.set_x(rect.get_x()+(i*(width/f_num)))
            i = i+1
    
                
    # plotting the legend
    def plotLegend(self,ax,li):
        leg = ax.legend(li, bbox_to_anchor=(-0.25, 1),
                        borderaxespad=0.,shadow=True)
        frame  = leg.get_frame()
        frame.set_facecolor('1.0')       # set the frame face color to white
        for t in leg.get_texts():
            t.set_fontsize('small')      # the legend text fontsize
        for l in leg.get_lines():
            l.set_linewidth(1.5)         # the legend line width
     
    
    # computes list of rel. frequency averages    
    def defineAvg(self,stats,f_num,c_num):
        means = []
        #for j in range(c_num):
            #meanj = 0
        for id in stats.keys():
            meanj = 0
            for i in stats[id]:
                    meanj = meanj + i
            meanj = (meanj/f_num)
            means.append(meanj)
        return means
    

    # computes list of rel. frequency averages    
    def defineBase(self,stats,f_num,c_num):
        means = []
        #for j in range(c_num):
            #meanj = 0
        for id in stats.keys():
            meanj = 0
            for i in stats[id]:
                    meanj = meanj + i
            meanj = (meanj/f_num)
            means.append(meanj)
        return means
    
    
    # computes sorted list of raw frequency averages    
    def defineAvg2(self,stats,f_num,c_num):
        means = []
        for j in range(c_num):
            meanj = 0
            for id in stats.keys():
                for i in stats[id]:
                    meanj = meanj + i
            meanj = ((meanj+1)/f_num)
            means.append(meanj)
        return means
        

################################################################################
    
    
# Class with the stats
class MMStats:
        
        
    # constructor
    def __init__(self):
        
        # 1. precision
            
        # precision by classifier and test (bars)       
        cls = {
              "Logit":  [0.63,0.62], "SVM":    [0.60,0.60],
              "Bayes":  [0.64,0.56], "Neural": [0.60,0.73],
              "Tree":   [0.69,0.72], "kNN":    [0.42,0.44]}       
        # averages: 0.59, 0.61

        # precision by feature and classifier (bars) on "unigram data"
        # logit, SMV, Bayes, Neural, Tree, kNN (k=10)     
        ftr = {
              "nest":   [0.64,0.60,0.64,0.63,0.69,0.42],
              "pos":    [0.64,0.59,0.64,0.62,0.69,0.43],
              "freq":   [0.64,0.60,0.64,0.64,0.70,0.46],
              "sub":    [0.63,0.60,0.65,0.65,0.69,0.42],
              "hd":     [0.65,0.57,0.64,0.63,0.71,0.42],
              "lf":     [0.62,0.60,0.64,0.60,0.70,0.41],
              "ls":     [0.57,0.55,0.57,0.57,0.56,0.42]}       
        # average: 0.59  
        
        # relation precision by feature and classifier (bars) 
        # logit, Bayes, Neural, Tree    
        rel = {
              "nest":   [0.44,0.40,0.50,0.66],
              "pos":    [0.50,0.38,0.40,0.66],
              "freq":   [0.45,0.42,0.40,0.66],
              "sub":    [0.55,0.45,0.66,0.66],
              "hd":     [0.36,0.23,0.50,0.30],
              "lf":     [0.25,0.33,0.41,0.66],
              "ls":     [0.45,0.45,0.40,0.71],
              "class":  [0.50,0.36,0.66,0.66]}     
        # average: 0.51
            
        self.expOne     = cls
        self.expTwo     = ftr
        self.expThree   = rel
  
        # 2. counts for stat tests
        
        clstest = {     
              "Logit":  [522,240], "Neural": [522,279],
              "SMV":    [512,242], "Tree":   [564,279],
              "Bayes":  [446,204], "kNN":    [347,154]
              }

        # logit, SMV, Bayes, Neural, Tree, kNN        
        ftrtest = {
              "nest":   [533,517,461,518,564,348],
              "pos":    [539,513,439,515,564,355],
              "freq":   [530,523,446,540,563,345],
              "sub":    [525,516,446,522,558,358],
              "hd":     [531,504,455,512,556,339],
              "lf":     [520,517,502,536,563,341],
              "ls":     [463,456,393,441,494,345]
              }
        
        # logit, Bayes, Neural, Tree
        reltest = {
              "nest":   [130,132,142,143],
              "pos":    [127,130,134,138],
              "freq":   [132,137,137,138],
              "sub":    [130,136,142,138],
              "hd":     [130,130,135,133],
              "lf":     [125,133,136,138],
              "ls":     [129,124,140,138],
              "class":  [131,129,148,143]}
        
        self.testOne     = clstest
        self.testTwo     = ftrtest
        self.testThree   = reltest
 
 
    # X^2 test(s)
    def tests(self):
        stats = STest()
        # results
        avgOne =    []
        for id in self.testOne.keys():
            avgOne.append(sum(self.testOne[id]))              
        avgTwo =    []
        for id in self.testTwo.keys():
            avgTwo.append(sum(self.testTwo[id]))            
        avgThree =  []
        for id in self.testThree.keys():
            avgThree.append(sum(self.testThree[id]))
        # tests
        # null hypothesis: uniform distribution
        # we want to know if it is random
        stats.myChiTest(avgOne,stats.uniFor(avgOne))
        stats.myChiTest(avgTwo,stats.uniFor(avgTwo))
        stats.myChiTest(avgThree,stats.uniFor(avgThree))