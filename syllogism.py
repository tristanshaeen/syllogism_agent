#################### syllogism production model ###################

# this is the simplest type of act-r model
# it uses only the production system and one buffer
# the buffer represents the focus of thought
# we call it the focus buffer but it is often called the goal buffer
# productions fire if they match the focus buffer
# each production changes the contents of focus buffer so a different production will fire on the next cycle


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
# create an act-r agent

class MyAgent(ACTR):
    
    focus=Buffer()
    DMbuffer=Buffer() # create a buffer for the declarative memory (henceforth DM)

    DM=Memory(DMbuffer)  # create DM and connect it to its buffer 

    focus.set('goal:syllogism step:conclusion')
    
    DM.add('premise:one subject:socrates isa:man')
    DM.add('premise:two subject:man isa:mortal')

    def conclusion(focus='goal:syllogism step:conclusion'):
        DM.add('conclusion:one subject:socrates isa:mortal')
        DM.request('conclusion:one subject:?subject isa:isa?')
        focus.set('goal:syllogism step:declare_conclusion')

    def declare_conclusion(focus='goal:syllogism step:declare_conclusion'):
        print(subject, isa)

tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
