#################### ham cheese production model ###################

# this is the simplest type of act-r model
# it uses only the production system and one buffer
# the buffer represents the focus of thought
# we call it the focus buffer but it is often called the task buffer
# productions fire if they match the focus buffer
# each production changes the contents of focus buffer so a different production will fire on the next cycle


import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

class MyEnvironment(ccm.Model):
    pass




class MyAgent(ACTR):

    focus=Buffer()
    DMbuffer=Buffer() 
    DM=Memory(DMbuffer,threshold=-15)            
   
    focus.set('task:syllogism subject:socrates isa:man')
    
    DM.add('subject:socrates isa:man')
    DM.add('subject:man isa:mortal')
            
    def DM_request(focus='task:syllogism subject:?subject isa:?isa'):
        print('the start of the syllogism is...')
        print('{} isa {}'.format(subject,isa))
        DMbuffer.set('state:empty')
        DM.request('subject:?isa')
        focus.set('task:syllogism subject_1:?subject') 

    def DM_retrieve(focus='task:syllogism subject_1:?subject_1',DMbuffer='subject:?subject_2 isa:?isa'): 
        print('{} isa {} and {} are {} so {} isa {}'.format(subject_1,subject_2,subject_2,isa,subject_1,isa))
        DMbuffer.set('state:empty')
        focus.set('task:stop')



tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
