"""
Created on Fri Jun 25 16:49:55 2021
@title:TSH-syllogism
@author: Steve

This model presents reasoning on the soundness of a syllogism, which is:
    Socrates is a man
    Man is mortal
    Therefore, Soctares is mortal
    
As a test, I modified the model to not have an environemnt to see what happens.
It works fine without an environment class instantiated
"""

#Set path to CCMSuite3 (on my computer. Different for other users)
import sys
sys.path.append('E:\Desktop\CCMSuite3-master')

import ccm  #Import the ccm modeling modules

from ccm.lib.actr import *  # Import the ACT-R modelling modules

# =============================================================================
# class MyEnvironment(ccm.Model):
#     pass #environemnt required but not used
# 
# =============================================================================

class MyAgent(ACTR):
    
    
    # Set attributes for the agent class
    focus=Buffer()
    IM1buffer = Buffer() #Imaginal buffer
    IM2buffer = Buffer() #Imaginal buffer
    IM1=Memory(IM1buffer, threshold=0) #Imaginal Memory
    IM2=Memory(IM2buffer, threshold=0) #Imaginal Memory
    DMbuffer=Buffer() #Declarative Memory nuffer
    DM=Memory(DMbuffer,threshold=0)  #Declarative memory          
       
    
    def init():
        """ 
        Intialize the agent production module
        Add the major and minor premises to declarative memory
        Set the focus buffer to 'start'
        """
        DM.add('premise:major subject:Socrates predicate:man')
        DM.add('premise:minor subject:man     predicate:mortal')
        focus.set('start')
    
    def request_major_premise(focus='start'):
        DM.request('premise:major subject:?subject predicate:?predicate')
        focus.set('state_major_premise')
        
    def state_major_premise(focus='state_major_premise',
                            DMbuffer= 'subject:?subject predicate:?predicate'):   
        print(f'The major premise is: {subject} is a {predicate}')
        """ Temproarily hold the subject, and predicate of the major premise in memory"""
        IM1.add('subject:?subject predicate:?predicate')
        focus.set('get_minor_premise')
         
    def request_minor_premise(focus='get_minor_premise'):
        DM.request('premise:minor subject:?subject predicate:?predicate')
        focus.set('state_minor_premise')

    def state_minor_premise(focus='state_minor_premise',
                            DMbuffer= 'subject:?subject predicate:?predicate'):   
        print(f'The minor premise is: {subject} is {predicate}')
        """Temporarily hold the subject and predicate of the minor premise in memory"""
        IM2.add('subject:?subject predicate:?predicate')
        focus.set('recall_subject')

    """
     Compare the predicate of the major premise with the subject of the minor premise
     to determine if it is indeed a logical syllogism
     In a Barbara style syllogism, the major premise predicate 
     and the minor premise subject must match.
    """

    def recall_minor_subject(focus='recall_subject'):
        # get the subject of the minor premise
        IM2.request('subject:?subject')
        focus.set('recall_predicate')
        
    def recall_major_predicate(focus='recall_predicate'):
        # Get predicate of major premise
        IM1.request('predicate:?predicate')
        focus.set('deduce')
        
  
    def deduce(focus='deduce',
               IM2buffer='subject:?subject2 predicate:?predicate2',
               IM1buffer='subject:?subject1 predicate:?predicate1'):
        #Compare the Major premise predicate to the minor premise subject
        print(f'If the subject of the minor premise is {subject2}')
        print(f'and the predicate of the major premise is {predicate1}')
        if subject2 == predicate1:
            #If they match, then the conclusion is logically sound
            print(f'therefore, the conclusion is \r\n      {subject1} is {predicate2}')
        else:
            print(' this is not a syllogism')
        focus.set('stop')

      
    def stop_run(focus='stop'):
        # End of production run
        print('Stop run')
        self.stop()
        
"""
NOTE: I have dropped the environment from the model since it is not used
Model runs fine without it. Don't know why yet.
"""
      
#env = MyEnvironment()          # name the environment
    
sophy = MyAgent()               # name the agent

#env.agent = sophy              # put the agent into the environment

#ccm.log_everything(env)        # print out what happens in the environment
ccm.log_everything(sophy)       # print out what happens to the agent

#env.run()                      # run the environment
sophy.run()                     # run  the agent              

ccm.finished()    