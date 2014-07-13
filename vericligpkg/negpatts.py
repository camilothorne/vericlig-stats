'''
Created on Jan 18, 2013

@author: camilothorne
'''

#===================#
#===================#
#                   #
#  NEG likelihoods  #
#                   #
#===================#
#===================#


# float division
from __future__ import division

# nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import brown
from nltk.tag.util import str2tuple
from nltk.tag import pos_tag
from nltk import word_tokenize, sent_tokenize
from nltk.tag import DefaultTagger, UnigramTagger, BigramTagger
from nltk.tag.sequential import NgramTagger

# string methods
import string, re, array
import itertools

# matplotlib
from matplotlib import pylab, cm
from numpy import *
from operator import itemgetter, attrgetter
import scipy
from math import ceil

# my classes
from corpuspkg.statsplot import MyPlot
from corpuspkg.statstests import STest


####################################################################


# N.B. We use Brown POS tags


s1 = ("not","*")
s2 = ("nobody","pn")
s3 = ("no","at")
s4 = ("","md*") # negated modal verb (many poss)!
s5 = ("none", "pn")
s6 = ("nothing", "pn")


####################################################################


# Class encoding the plot


class NegStats:
   
    
    # corpus       : path to corpora
    # format       : format of corpora (e.g. .txt files)
    # stats        : hash table with class stats of each corpus
    # classstats   : list with global stats (mean frequency) 
    
    
    # object constructor
    def __init__(self,path,format):
        self.stats = {}
        self.classstats = []
        self.path = path
        self.format = format
        self.occStats(path,format) # collects stats + plots them
        self.statTest(self.classstats) # runs the stat tests
    
    
    #############################################################
    
    
    # collecting statistics
    def occStats(self,path,format):
        wordlists = PlaintextCorpusReader(path,format)
        fileids = wordlists.fileids()
        k = len(fileids)
        # computing rel frequencies
        self.fileStats(path,fileids)
        # plotting
        MyPlot(self.stats,self.classstats,"Negations", "two") 
    
            
    # creating the classes
    def fileStats(self,path,fileids):
        # starting the tagger
        my_tagger = Tagger().t3
        # stat classes
        C1 = MyClassStats2("guideline",[],0)
        C2 = MyClassStats2("business",[],0)
        C3 = MyClassStats2("brown",[],0)
        self.classstats = [C1,C2,C3]        
        print "###################################################"
        print "NEGs STATS"
        print "###################################################"
        # computing the stats
        for id in fileids:
            ####################################################################
            filestats = []
            ####################################################################
            print "==================================================="
            print id
            print "==================================================="
            # corpus
            #-------------------------------------------------------------------
            corpus = MyClass2([],[],id,0,0,"corpus","A",my_tagger)
            print "---------------------------------------------------"
            print "A. Computing corpus size"
            print "---------------------------------------------------"
            corpus.openFile(path+"/"+id,corpus.pats,corpus.patts)        
            print "==> " + id + " is of size : " + `corpus.count` + " word tokens"
            ####################################################################            
            # patterns
            pew = [s1,s2,s3,s4,s5,s6]
            rest = []          
            ####################################################################
            # class 1
            P1 = MyPatts2(pew).P
            N1 = MyPatts2(rest).P
            #-------------------------------------------------------------------
            c1 = MyClass2(P1,N1,id,0,0,"guideline","B",my_tagger)
            print "---------------------------------------------------"
            print "B. computing class 1"
            print "---------------------------------------------------"
            c1.openFile(path+"/"+id,c1.pats,c1.patts)
            c1.freq = (c1.count/corpus.count)
            print "==> NEGs : " + `c1.count` + " cum. word tokens"
            print "==> NEGs : " + `c1.freq` + " rel. freq."
            ####################################################################
            # class 2
            P2 = MyPatts2(pew).P
            N2 = MyPatts2(rest).P
            #-------------------------------------------------------------------       
            c2 = MyClass2(P2,N2,id,0,0,"business","C",my_tagger)
            print "---------------------------------------------------"
            print "C. computing class 2"
            print "---------------------------------------------------"
            c2.openFile(path+"/"+id,c2.pats,c2.patts)
            c2.freq = (c2.count/corpus.count)
            print "==> NEGs : " + `c2.count` + " cum. word tokens"
            print "==> NEGs : " + `c2.freq` + " rel. freq."
            ####################################################################
            # class 3
            P3 = MyPatts2(pew).P
            N3 = MyPatts2(rest).P
            #-------------------------------------------------------------------
            c3 = MyClass2(P3,N3,id,0,0,"brown","D",my_tagger)
            print "---------------------------------------------------"
            print "D. computing class 3"
            print "---------------------------------------------------"
            c3.openFile(path+"/"+id,c3.pats,c3.patts)
            c3.freq = (c3.count/corpus.count)
            print "==> NEGs : " + `c3.count` + " cum. word tokens"
            print "==> NEGs : " + `c3.freq` + " rel. freq."
            ####################################################################
            filestats = [c1,c2,c3]
            ####################################################################  
            self.stats[id] = filestats
            ####################################################################  
            for aclass in self.classstats:
                for thiscls in filestats:
                    if ((thiscls.tag == aclass.tag) & (thiscls.count > 0)):
                        aclass.classes.append(thiscls)
        print "###################################################"
        # updating the distribution 
        self.classAvg(self.classstats)
        self.classAvg2(self.classstats)
        sort = self.sortClass(self.classstats)
        self.classstats = sort
        self.printClasses(self.classstats)
        

    ############################################################# 
        
                
    # sorts stats classes
    def sortClass(self,classlist):
        sort = sorted(classlist,key=attrgetter('avg'))
        return sort
    
    
    # computes list of averages    
    def classAvg(self,classstats):
        for cla in classstats:
            meanj = 0
            for id in cla.classes:
                meanj = meanj + id.freq
            meanj = (meanj/len(cla.classes))
            cla.avg = meanj
            
            
    # computes list of frequencies    
    def classAvg2(self,classstats):
        for cla in classstats:
            meanf = 0
            for id in cla.classes:
                meanf = meanf + id.count
            meanf = (meanf/len(cla.classes))
            cla.fre = meanf
    
    
    #############################################################
    
        
    # prints the stats
    def printClasses(self,classstats):
        for cla in classstats:
            print cla.tag
            print "---------------------------------------------------"            
            print `cla.avg` + ": avg rel. freq"
            print "---------------------------------------------------"
            for id in cla.classes:
                print `id.freq` + ": rel. freq "+ id.fileid
                print `id.count` + ": freq "+ id.fileid              
            print "###################################################"


    #############################################################

        
    # statistical tests
    def statTest(self,classstats):
        
        s = STest()
        
        # we populate the samples
             
        # PEWs freqs per corpus     
        sample1 = [] 
        for cla in classstats:
            for cl in cla.classes:
                sample1.append(cl.count)
                
        # contingency table, corpus x PEWs freq
        sample2 = []
        for cla in classstats:
            for cl in cla.classes:
                sample2.append([cl.count, 
                                int(ceil(cl.count/cl.freq)-cl.count)
                                ])
                
        # PEWs rel. freqs per corpus
        sample3 = []
        for cla in classstats:
            for cl in cla.classes:
                sample3.append(cl.freq)
                
        # contingency table, corpus type x PEWs freq        
        sample4 = []
        for cla in classstats:
            h       = sum([cl.count for cl in cla.classes])
            non_h   = sum([ceil(cl.count/cl.freq) for cl in cla.classes])-h
            sample4.append([h,int(non_h)])
            
        # we call the stats methods
        
        print "Statistical tests:"
        
        s.mySkew(sample1)       # skewness
        print "---------------------------------------------------"
        print "sam = ",sample1,"\n(NEGs freqs per corpus)"       
        s.myTTest(sample1,0.005)  # one-way t test
        print "---------------------------------------------------"
        print "sam = ",sample1,"\n(NEGs freqs per corpus)"
        s.myChiInd(sample2)     # X^2 for independence
        print "---------------------------------------------------"
        print "sam = ",sample2,"\n(contingency table, corpus x NEGs freq)"
        s.myEntropy(sample3)    # entropy
        print "---------------------------------------------------"
        print "sam = ",sample3,"\n(NEGs rel. freqs per corpus)"
        s.myChiInd(sample4)     # X^2 for independence
        print "---------------------------------------------------"
        print "sam = ",sample4,"\n(contingency table, corpus type x NEGs freq)"
    
        
####################################################################


# Class collecting stats        
class MyClass2:


    #fileid:   filename
    #count :   feature occ frequency
    #freq  :   feature occ rel frequency
    #pats  :   set of regexps whose occ we want to check
    #patts :   set of regexps whose occ we want to rule out
    #tag   :   class name tag
    #typ   :   corpus type
    #tagger:   POS tagger for mining


    # object constructor
    def __init__(self,pats,patts,fileid,count,freq,tag,typ,tagger):
  
        
        self.pats = pats
        self.patts = patts
        self.fileid = fileid
        self.count = count
        self.freq = freq
        self.tag = tag
        self.typ = typ
        self.tagger = tagger
  
        
    # open file method   
    def openFile(self,fileid,pats,patts):
        
        lcount = 0
        file = open(fileid,'r')
        my_tagger = self.tagger
        
        # case 0 (counting word tokens)
        if self.typ == "A":
            try:
                text = file.read()
                tokens = word_tokenize(text)
                lcount = len(tokens)
            finally:
                self.count = lcount
                file.close()
                
        # case 1 (non-pos-tagged, domain specific)
        if ((self.typ == "B") & (re.search("-dom-",fileid) != None)):
            try:
                text = file.read()
                lines = sent_tokenize(text)
                res = []
                for line in lines:
                    res = res + my_tagger.tag(line.split())
                for pa in pats:
                    for tup in res:
                        if (tup[1] == pa[1]) & (tup[0] == pa[0]) & (pa[1] != 'md*'):
                            lcount = lcount + 1
                        if (pa[1] == 'md*') & (pa[1] == tup[1]):
                            lcount = lcount + 1
            finally:
                self.count = lcount
                file.close()
                
        # case 2 (non-pos-tagged, open domain)
        if ((self.typ == "C") & (re.search("-open-",fileid) != None)):
            try:
                text = file.read()
                lines = sent_tokenize(text)
                res2 = []
                for line in lines:
                    res2 = res2 + my_tagger.tag(line.split())
                for pa in pats:
                    for tup in res2:
                        if (tup[1] == pa[1]) & (tup[0] == pa[0]) & (pa[1] != 'md*'):
                            lcount = lcount + 1
                        if (pa[1] == 'md*') & (pa[1] == tup[1]):
                            lcount = lcount + 1
            finally:
                self.count = lcount
                file.close()
                
        # case 3 (pos-tagged, open domain)
        if ((self.typ == "D") & (re.search("-pos-",fileid) != None)):
            try:
                text = file.read()
                res = [str2tuple(t) for t in text.split()]
                for pa in pats:
                    for tup in res:
                        if (tup[1] == pa[1]) & (tup[0] == pa[0]) & (pa[1] != 'md*'):
                            lcount = lcount + 1
                        if (pa[1] == 'md*') & (pa[1] == tup[1]):
                            lcount = lcount + 1
            finally:
                self.count = lcount
                file.close()


####################################################################    

    
# Class training POS taggers        
class Tagger:
        
        
        #train     : traininig corpus
        #t0        : uniform tagger
        #t1        : unigram (MLE) tagger
        #t3        : bigram  (MLE) tagger
        
        
        # constructor
        def __init__(self):
            self.train = brown.tagged_sents(categories='news')
            self.t0 = DefaultTagger('None')
            self.t1 = UnigramTagger(self.train,backoff=self.t0)
            self.t2 = BigramTagger(self.train,cutoff=2,backoff=self.t1)
            self.t3 = NgramTagger(3,train=self.train,backoff=self.t2)
        
            
        # evaluate tagger accuracy
        def eval(self):
            self.gold = brown.tagged_sents(categories=['editorial','fiction'])
            acc0 = self.t2.evaluate(self.gold)
            acc1 = self.t2.evaluate(self.gold)
            acc2 = self.t3.evaluate(self.gold)
            print '1-gram (acc) = ' + `acc0`
            print '2-gram (acc) = ' + `acc1`
            print '3-gram (acc) = ' + `acc2`      


####################################################################

            
# Class encapsulating lists of patterns        
class MyPatts2:
    
    
        #P : list of regular expressions
        P = []
    
        
        # constructor
        def __init__(self,S):
            B = []
            for s in S:
                B.append(s)
            self.P = B


####################################################################


# Class encapsulating all the class stats
class MyClassStats2:
    
    
    #classes:    list of classes
    #avg:        average
    #tag:        class tag
    #typ:        corpus subset

    
    # constructor
    def __init__(self,tag,classes,avg):
        self.tag = tag
        self.classes = classes
        self.avg = avg
        self.fre = 0

