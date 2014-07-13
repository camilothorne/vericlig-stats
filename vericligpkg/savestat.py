'''
Created on Jul 20, 2013

@author: camilothorne
'''

#import re, string, array
from subprocess import call, Popen


class SaveStat:
    
    
    # path         : path to report file
    # plotfile     : path to the plots
    # tables       : path to the table
    
    
    # constructor
    def __init__(self,table,plotfile1,plotfile2,name):
        self.path       = "/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/compiled/"+name+ ".tex"
        self.plotfile1   = plotfile1
        self.plotfile2   = plotfile2
        self.table      = table
        # building the report
        res = self.makeRes(self.table, self.plotfile1, self.plotfile2, name)
        # saving the report
        print "###################################################"
        print "\n\npreparing report...\n\n"
        self.compileFile(self.path, res)
        self.fileSave(self.path, res)
        
    # make contingency table   
    def makeRes(self,table,plotfile1,plotfile2,name):
                        
        # plugin table
        title = r'\begin{center}\textbf{\Huge '+name+'}\end{center}\n'
        ntable  = title + r'\begin{sidewaystable}[p]' + "\n" #+ "\centering\n\n"
        #print table
        myfile  = open(table,'r')
        myfiler = myfile.read()
        ntable  = ntable + myfiler
        ntable  = ntable + "\end{sidewaystable}\n\n"
        myfile.close()     
        # complete and return table 
        fig1 = r'\begin{center}' + "\n\includegraphics[scale=1.0]{" + plotfile1 + "}\n\end{center}\n"
        fig2 = r'\begin{center}' + "\n\includegraphics[scale=1.0]{" + plotfile2 + "}\n\end{center}\n"
        res = ntable + "\n\n" + r'\vspace{0.2cm}' + "\n\n" + fig1 + "\\newpage\n" + fig2
        return res    
        
    
    # save the table in a .tex file    
    def fileSave(self,path,res):
        myfile = open(path,'w')
        myfile.write(res)
        myfile.close()
    
        
    # compile with pdflatex
    def compileFile(self,path,res):
        myfile = open(path,'w')
        myfile.write("\documentclass[a4,10pt]{article}")
        myfile.write("\n\n")
        myfile.write("\usepackage{graphicx}\n")
        myfile.write("\usepackage{epstopdf}\n")
        myfile.write("\usepackage{rotating}\n")
        myfile.write("\usepackage{times}\n")
        myfile.write("\n\n")
        myfile.write(r'\begin{document}')
        myfile.write("\n\n")
        myfile.write(res)
        myfile.write("\n\n")
        myfile.write("\end{document}")
        myfile.close()
        call(['/opt/local/bin/pdflatex',
              '-output-directory=/home/camilo/Desktop/Com-Sem-Frams/meta-map/meta-map-gold/compiled/',
              path],
             shell=False)      
