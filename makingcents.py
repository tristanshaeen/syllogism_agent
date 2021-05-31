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
# create our basic syllogism solver -> precursor to tristan's model


class MyAgent(ACTR):
    focus=Buffer()
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer    
    
    def init():                                             
        DM.add ('Q causes R')
        
        DM.add ('P causes Q')
        focus.set('begin')

    def can_i_haz_sum_logickz(focus='begin'):
        print ('Im connecting the dots')  
        DM.request('? causes ?') # requesting a chunk containing info of the form X causes Y   
        focus.set('remember')
                

    def mental_ize(focus='remember', DMbuffer='?A causes ?B',DM='busy:False'): #dm chunk requested in can_i_haz_sum_logickz 
        print ( A + " causes " + B)   
        DM.request('?B causes ?') #check for an antecedent of the antecedent
        focus.set('?A causes ?B')   #put retrieved fact in focus
        
    def compare_your_minds (focus='?A causes ?B', DMbuffer='?C causes ?D'): # focus and dm from mental_ize production
        print ("and " + C + " causes " + D)
        if B == C: # could use buffers + extra productions to make more cognitive - I'm lazy so I used if/else
            print ( A + ' causes ' + D)   
            DM.add('?A causes ?D')
            print ("I have seen through your lies")
            self.focus.set('stop') #self because you need to refer back to the agent after indentation - idk why -> stops after making a connection
        else:
            self.focus.set('begin') #if b is not equal to c then prior DM retrieval made an error -> start from the top

    def false_memory (focus='?A causes ?B', DM='error:True'): #if no fact matches search at production mental_ize
        print ('no not that')  
        DM.request('? causes ?A')   #see if precendent is an antecedent to something else
        focus.set('remember')

    def stop_production(focus='stop'):
        self.stop()



tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
