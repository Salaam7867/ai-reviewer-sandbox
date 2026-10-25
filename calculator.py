import os
import sys

def process_user_input(user_data, cache=[]):
    # SECURITY ISSUE: eval() is highly dangerous
    result = eval(user_data)
    
    # BUG: mutable default argument 'cache' will cause memory leaks
    cache.append(result)
    
    # HYGIENE: unused import (sys), bad spacing
    print( "Done" )
