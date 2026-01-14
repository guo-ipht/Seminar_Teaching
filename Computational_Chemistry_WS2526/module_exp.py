
def max_min(x):
    """
    This function finds the maximum and minimum items of an input list
    return two values, maximum and minimum, respectively
    """
    print("calling function from module 'module_exp'")
    current_max = x[0]   
    current_min = x[0]   
    for v in x:         
        
        if v>current_max:     
            current_max = v   
    
        elif v<current_min:   
            current_min = v   

        else:                 
            continue          
        
    return current_max, current_min