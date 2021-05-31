#################### ham cheese instruction model ###################

# this model uses the contents of DM to decide what to do next
# the productions are generic and capable of following any instructions from DM

import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

#####
# Python ACT-R requires an environment
# but in this case we will not be using anything in the environment
# so we 'pass' on putting things in there

class MyEnvironment(ccm.Model):
    pass

#####
# funnier syllogism model precursor -> answers a question -> sometimes engages in some funny circular reasoning.
#No I won't be making any more comments from here -> have fun


class MyAgent(ACTR):
    focus=Buffer()
    DMbuffer=Buffer()
    Qbuffer=Buffer()
    cbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer    
    
    def init():
        DM.add ('P causes R Doesit')                                             
        DM.add ('Q causes R')                     
        DM.add ('P causes Q')
        DM.add ('A causes B')
        DM.add ('A causes D')
        DM.add ('D causes B')
        focus.set('begin')

    def can_i_haz_sum_logickz(focus='begin'):
        print ('Im connecting the dots')  
        DM.request('? causes ? Doesit')    
        focus.set('remember')
    
    def my_quest(focus='remember', DMbuffer='?A causes ?B Doesit',DM='busy:False'):
        print ("Does " + A + " cause " + B + "?")   
        DM.request('?A causes ?')
        Qbuffer.set('?A causes ?B Doesit')        
        focus.set('remember') 

    
    
    def my_test_A(focus='remember', Qbuffer='?A causes ?B Doesit', DMbuffer = "?C causes ?D", DM='busy:False'):
        cbuffer.set("?A ?C")
        DM.request("?C causes ?D")
        Qbuffer.set("'?A causes ?B Doesit'")
        print ("Is " + A + " " + C + "?")
        focus.set("remember1")

    def my_test_win(focus='remember1', Qbuffer='?A causes ?B Doesit', DMbuffer = "?C causes ?D", DM='busy:False', cbuffer ='?E ?E'):
            print ( A + " causes " + D)   
            DM.request('?D causes ?')
            self.focus.set('?A causes ?D')

    def my_test_win(focus='remember1', Qbuffer='?A causes ?B Doesit', DMbuffer = "?C causes ?D", DM='busy:False', cbuffer ='?E ?F'):
            DM.request("?A causes ?")
            self.focus.set('remember') 
   
    def compare_your_minds (focus='?A causes ?B', DMbuffer='?C causes ?D', Qbuffer = '?E causes ?F Doesit'):
        print ("and " + C + " causes " + D)
        if B == C:
            print ( A + ' causes ' + D)   
            DM.add('?A causes ?D')
            if E == A and D == F:    
                print ("Yes, " + E + " causes " + F)
                self.Qbuffer.set('')
                self.focus.set('stop')
            else:
                self.focus.set('remember')
        else:
            self.focus.set('remember')              
    
    def false_memory (focus='?A causes ?B', DM='error:True'):
        print ('no not that')  
        DM.request('? causes ?A')    
        focus.set('remember')
    
    def stop_production(focus='stop'):
        self.stop()



tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
