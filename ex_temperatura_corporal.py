# 
# Author: Fabrício G. M. C - Ph.D

# The internal state corresponds to
# temperature history.
# The environment model is expressed
# in the conditiion-action rules

class ModelBasedReflexAgent:
    def __init__(self, temp):
        # internal state
        self.last_temp = temp

    def select_action(self, temp):
        if (temp - self.last_temp) > 0:
            temp_increase = True
        else:
            temp_increase = False
        # internal state update:
        if temp_increase and temp > 37.5:
            return "Strong medication"
        elif not temp_increase and temp > 37.5:
            return "Mild medication"
        elif temp <= 37.5:
            return "No medication"

# This agent has no internal state
# (i.e.: memory) nor environment model.
class ReflexAgent:
    def __init__(self):
        pass
    def select_action(self,temp):
        if temp > 37.5:
            return "Mild medication"
        else:
            return "No medication"
            
