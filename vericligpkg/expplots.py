'''
Created on May 2, 2013

@author: camilothorne
'''


# python
from __future__ import division
import array
from matplotlib import pylab, cm, rc
from numpy import *
from operator import itemgetter, attrgetter
import scipy
import csv
from time import time


# statistical test(s)
from corpuspkg.statstests import *


# saving the experiments
from savestat import *


# Class encoding the plots
class ExpPlotC:
     
     
    #constructor
    def __init__(self):
        mys = MMStats()
        
        statsA = mys.expOne
        statsB = mys.expTwo
        statsC = mys.expThree
        statsAF = mys.expOneF
        statsBF = mys.expTwoF
        statsCF = mys.expThreeF
        
        
        uni = mys.titOne
        bis = mys.titTwo
        rel = mys.titThree
        uniF = mys.titOneF
        bisF = mys.titTwoF
        relF = mys.titThreeF
        
        
        rc('xtick', labelsize=12) 
        rc('ytick', labelsize=12) 
                
                
        fig1 = pylab.figure(figsize=(5,5), dpi=100)
        fig2 = pylab.figure(figsize=(5,5), dpi=100)
        fig3 = pylab.figure(figsize=(5,5), dpi=100)      
        fig4 = pylab.figure(figsize=(5,5), dpi=100)
        fig5 = pylab.figure(figsize=(5,5), dpi=100)
        fig6 = pylab.figure(figsize=(5,5), dpi=100)   
        
        
        self.plotCurve(fig1,statsA,len(statsA[0]),"Noun Phrases" ,1)     
        self.plotCurve(fig2,statsB,len(statsB[0]),"Sentences"    ,1)
        self.plotCurve(fig3,statsC,len(statsC[0]),"Relations"    ,1)
        self.plotBar(fig4,statsA,statsAF,5,len(statsAF),"Noun Phrases" ,1)     
        self.plotBar(fig5,statsB,statsBF,5,len(statsBF),"Sentences"    ,1)
        self.plotBar(fig6,statsC,statsCF,5,len(statsCF),"Relations"    ,1)
     
        
        pylab.ioff()
        
        #mys.tests()
        
        #to use if needed
        #mytime = '%.2f' % time()
        mytime = ""
        
        
        fig1.savefig('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+uni+mytime+'.pdf')
        fig2.savefig('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+bis+mytime+'.pdf')      
        fig3.savefig('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+rel+mytime+'.pdf')     
        fig4.savefig('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+uniF+mytime+'.pdf')
        fig5.savefig('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+bisF+mytime+'.pdf')      
        fig6.savefig('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+relF+mytime+'.pdf')    
        
        pylab.show()


        # compiling Latex report        
        SaveStat('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+uni+mytime+'.tex',
                 '/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+uni+mytime+'.pdf',
                 '/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+uniF+mytime+'.pdf',
                 "NPhrase")
        SaveStat('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+bis+mytime+'.tex',
                 '/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+bis+mytime+'.pdf',
                 '/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+bisF+mytime+'.pdf',                 
                 "Sentence")
        SaveStat('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+rel+mytime+'.tex',
                 '/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+rel+mytime+'.pdf',
                 '/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+relF+mytime+'.pdf',                 
                 "Relation")        
        
                                    
    # 1. curve chart plotter
    #
    # feature x precision, recall, f-measure, accuracy (averages)   
    def plotCurve(self,figu,stats,c_num,name,pos):
        
        ax = figu.add_subplot(1,1,pos)
        ind = pylab.arange(c_num)
        width = 1   # 1cm per unit of length
        maxi = 0.75    # y-axis ranges from 0 to 0.8
        
        # tags, precision, recall, fmeasure and accuracy
        ctags   = stats[0]
        pre     = stats[1]
        rec     = stats[2]
        fme     = stats[3]
        acc     = stats[4]
        
        # line identifiers
        li = ("Pr","Re","F1","Ac")    
                              
        # plot precision
        ax.plot((ind+width/2),pre,'o--',# change line type
                color='r',linewidth=3,label="Pr") # change color
        # plot recall
        ax.plot((ind+width/2),rec,'x-',# change line type
                color='b',linewidth=1,label="Re") # change color
        # plot F measure
        ax.plot((ind+width/2),fme,'o-',# change line type
                color='g',linewidth=3,label="F1") # change color
        # plot accuracy
        ax.plot((ind+width/2),acc,'x--',# change line type
                color='k',linewidth=1,label="Ac") # change color
                
        # setting axis
        if name=="Relations":
            ax.axis([0,c_num,0,maxi])
        else:
            ax.axis([0,c_num,0.5,maxi])
            
        # set name of y-axis
        ax.set_ylabel(name+" (avg.)",fontsize='12')
        
        # plot feature names
        mytags = []
        for c in range(c_num):
            mytags.append(c+(width/2))
        ax.set_xticks(mytags)
        ax.set_xticklabels(ctags,rotation='45',fontsize='12')
        ax.grid(False)
     
        # plot legend
        self.plotLegend(ax,li)
 
 
    # 2. bar chart plotter
    #
    # classifier x feature x f-measure 
    def plotBar(self,figu,means,stats,f_num,c_num,name,pos):
        
        ctags   = means[0]
        pre     = means[1]
        rec     = means[2]
        fme     = means[3]
        
        ax = figu.add_subplot(1,1,pos)
        ind = pylab.arange(c_num)
        width = 1
        i = 0
        maxi = 0.8
        mytags = []
        
        # plot bars
        self.barPlot3(ax,ind,width,f_num,stats,i)
        
        # plot mean precision
        ax.plot((ind+width/2),pre,'x-',# change line type
                color='r',linewidth=1,label="Pr") # change color
        # plot mean recall
        ax.plot((ind+width/2),rec,'x-',# change line type
                color='b',linewidth=3,label="Re") # change color
        # plot mean F measure
        ax.plot((ind+width/2),fme,'x-',# change line type
                color='g',linewidth=5,label="F1") # change color

        # setting axis
        if name=="Relations":
            ax.axis([0,c_num,0,maxi])
        else:
            ax.axis([0,c_num,0.5,maxi])
        
        # setting axis label
        ax.set_ylabel("F1-measure ("+name+")",fontsize='12')
        
        # plot class names
        for c in range(c_num):
            mytags.append(c+(width/2))
        ax.set_xticks(mytags)
        ax.set_xticklabels(ctags,rotation='45',fontsize='12')
        ax.grid(False)
        
        li = ('Pr','Re', 'F1','Logit','SVM','Bayes','Neural','Tree')
        
        # plot legend
        self.plotLegend(ax,li)
 
            
    # plotting the bars in the chart
    def barPlot3(self,ax,ind,width,f_num,stats,i):
        cstats = []
        for i in range(f_num):
            cstats.append([])
        for i in range(f_num):
            for id in stats:
                cstats[i].append(id[i])
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
        #leg = ax.legend(li,shadow=True,loc=0)
        leg = ax.legend(li,bbox_to_anchor=(0., 1.005, 1., .102), loc=3,
                        ncol=4, mode="expand", borderaxespad=0.)
        frame  = leg.get_frame()
        frame.set_facecolor('1.0')       # set the frame face color to white
        for t in leg.get_texts():
            t.set_fontsize('large')      # the legend text fontsize
        for l in leg.get_lines():
            l.set_linewidth(1.5)         # the legend line width
     
    

################################################################################
    
    
# Class with the stats
class MMStats:
        
        
    # constructor
    def __init__(self):
 
        
        # set data for plots (10-fold cross)       
        self.expOne     = self.readAVG("activity-10cross")
        self.titOne     = "activity-10cross"
        self.expTwo     = self.readAVG("activity-con-10cross")
        self.titTwo     = "activity-con-10cross"
        self.expThree   = self.readAVG("relation-10cross")
        self.titThree   = "relation-10cross"


        # set data for charts (10-fold cross)       
        self.expOneF     = self.readF("activity-10crossF")
        self.titOneF     = "activity-10crossF"
        self.expTwoF     = self.readF("activity-con-10crossF")
        self.titTwoF     = "activity-con-10crossF"
        self.expThreeF   = self.readF("relation-10crossF")
        self.titThreeF   = "relation-10crossF"


#        # set data for plots (custom)  
#        self.expOne     = self.readAVG("activity-custom")
#        self.titOne     = "activity-custom"
#        self.expTwo     = self.readAVG("activity-con-custom")
#        self.titTwo     = "activity-con-custom"
#        self.expThree   = self.readAVG("relation-custom")
#        self.titThree   = "relation-custom"
#
#
#        # set data for charts (custom)  
#        self.expOneF     = self.readF("activity-customF")
#        self.titOneF     = "activity-customF"
#        self.expTwoF     = self.readF("activity-con-customF")
#        self.titTwoF     = "activity-con-customF"
#        self.expThreeF   = self.readF("relation-customF")
#        self.titThreeF   = "relation-customF"
  

    # open data file (classifier averages)
    def readAVG(self,name):
        readerA = open('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+name+'.csv', 'rb')
        feats   = self.csv_extract_col(readerA, 'avg')
        readerB = open('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+name+'.csv', 'rb')
        pre     = [float(i) for i in self.csv_extract_col(readerB, 'Pr')]
        readerC = open('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+name+'.csv', 'rb')
        rec     = [float(i) for i in self.csv_extract_col(readerC, 'Re')]
        readerD = open('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+name+'.csv', 'rb')
        f_1     = [float(i) for i in self.csv_extract_col(readerD, 'F1')]
        readerE = open('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+name+'.csv', 'rb')
        acc     = [float(i) for i in self.csv_extract_col(readerE, 'Ac')]
        #print feats
        #print pre
        #print rec
        #print f_1
        #print acc
        res     = [feats,pre,rec,f_1,acc]
        return res
    
    
    # extract columns    
    def csv_extract_col(self,csvinput,colname):
        col = []
        for row in csv.DictReader(csvinput,delimiter = ",", quotechar = "'"):
            col.append(row[colname])
        return col
    
    
    # open data file (F measure)
    def readF(self,name):
        csvinput = open('/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/experiments/'+name+'.csv', 'rb')
        rows = []
        data = []
        for row in csv.reader(csvinput):
            data.append(row)
        for d in data[1:]:
            vals = [float(i) for i in d[1:]]
            rows.append(vals)
        return rows    
    
 
 
################################################################################
 
 
#    # missing: contingency table with counts!!!
# 
# 
#    # X^2 test(s)
#    def tests(self):
#        stats = STest()
#        
#        # results
#        avgOne =    []
#        for id in self.testOne.keys():
#            avgOne.append(sum(self.testOne[id]))              
#        avgTwo =    []
#        for id in self.testTwo.keys():
#            avgTwo.append(sum(self.testTwo[id]))            
#        avgThree =  []
#        for id in self.testThree.keys():
#            avgThree.append(sum(self.testThree[id]))
#            
#        # tests
#        # null hypothesis: uniform distribution
#        # we want to know if it is random
#        stats.myChiTest(avgOne,stats.uniFor(avgOne))
#        stats.myChiTest(avgTwo,stats.uniFor(avgTwo))
#        stats.myChiTest(avgThree,stats.uniFor(avgThree))