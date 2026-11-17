import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def max_min(x):
    """
    This function finds the maximum and minimum items of an input list
    return two values, maximum and minimum, respectively
    """
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

#### distributions
def check_distributions(n_sample=50, dist=['Uniform', 'Gaussian', 'Poisson', 'Binomial']):
    
    if dist not in ['Uniform', 'Gaussian', 'Poisson', 'Binomial']:
        print('currently only support Uniform, Gaussian, or Poisson distribution')

    if dist=='Uniform': ### here simulate 6-value dice
        val = np.random.randint(low=1, high=7, size=n_sample)
        expectation = (1+6)/2.0
        variance = (6**2-1)/12.0   
    elif dist=='Gaussian':
        val = np.random.normal(0, 1, size=n_sample)
        expectation = 0
        variance = 1
    elif dist=='Poisson':
        val = np.random.poisson(lam=1, size=n_sample)
        expectation = 1
        variance = 1
    elif dist=='Binomial':
        val = np.random.binomial(n=100, p=0.01, size=n_sample)
        expectation = 100*0.01
        variance = 100*0.01*(1-0.01)

    print('expectation = ' + str(expectation))
    print('empirical mean = ' + str(np.mean(val)))
    print('variance = ' + str(variance))
    print('sample variance = ' + str(np.var(val)))
    return val

### generate random variables following normal distribution and plot
def gen_random(n_sample=50, list_mean=[0, 0.1, 2], list_var=[1, 1, 1]):

    if len(list_mean)!=len(list_var):
        list_var = list_var[0]*len(list_mean)

    ### create colors
    colors = mpl.colormaps['coolwarm']
    colors = colors(np.linspace(0, 1, len(list_mean)))

    ### prepare figure to plot
    fig = plt.figure(figsize=(4, 3))

    S_all = []
    for i in range(len(list_mean)):
        ### normal distributed variable
        S = np.random.normal(list_mean[i], list_var[i], n_sample)
        S_all.append(S)
        ### plot data
        plt.scatter([i+1]*n_sample, S, color=colors[i])
        plt.plot([i+1-0.25, i+1+0.25], [list_mean[i], list_mean[i]], color=colors[i])
       
    plt.xticks(np.array(range(len(list_mean)))+1, labels=['S' + str(i+1) for i in range(len(list_mean))])
    plt.title('sample size: ' + str(n_sample))
    plt.show()

    return S_all

def gauss_func(x, O, A, b, c):
    """
    Parameters
    ----------
    x : numpy array
        input xaxis.
    O, A, b, c : int
        Initialization values.

    Returns
    -------
    numpy array
        Corresponding values using Gaussian function.
    """
    return O + A * np.exp(-(x - b) ** 2 / (2 * c ** 2))
   
def lorentz_func(x, O, A, b, c):
    """
    Parameters
    ----------
    x : numpy array
        input xaxis.
    O, A, b, c : int
        Initialization values.

    Returns
    -------
    numpy array
        Corresponding values using Lorentzian function.

    """
    return O + A * c / ((c ** 2) + (b - x) ** 2)