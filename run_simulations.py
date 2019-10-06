import numpy as np
import time 
import abm_variable_fitness as sim  

###############################################################################
# User inputs
drugless_path = "C:\\Users\\Eshan\\Documents\\python scripts\\theory division\\abm_variable_fitness\\data\\ogbunugafor_drugless.csv"
#ic50_path = "C:\\Users\\Eshan\\Documents\\python scripts\\theory division\\abm_variable_fitness\\data\\cycloguanil_ic50.csv"
ic50_path = "C:\\Users\\Eshan\\Documents\\python scripts\\theory division\\abm_variable_fitness\\data\\pyrimethamine_ic50.csv"

# good defaults
#n_mutations = 2
#n_deaths = n_mutations*100
#n_gen=2000  # Number of simulated generations
#const_dose = 100

# try other defaults

# n_mutations and n_deaths comes from me playing around with the idea of these 
# simulations being scale-invariant. You can comment them out and use mut_rate 
# death_rate instead.
n_mutations = 6
n_deaths = n_mutations*50
n_gen=2000 # Number of simulated generations
#const_dose = np.array([0,10**-3,10**-2,10**-1,1,100,200])
const_dose = np.array([200])

mut_rate=n_mutations/n_gen  # probability of mutation per generation
death_rate=n_deaths/n_gen  # Death rate
max_cells=10**5  # Max number of cells

init_counts = np.zeros(16)
init_counts[0] = 10000

carrying_cap=True
plot = False # False - plot the final averaged result only. True - plot every simulation result
curve_type = 'constant'
log_scale = True # put the drug concentration on a log-scale

# Parameters for non-linear curves
slope=10000
max_dose = 1000
min_dose = 0
h_step = 100

# number of simulations to average results together.  
n_sims = 10
###############################################################################
# End user inputs
drugless_rates = sim.load_fitness(drugless_path)
ic50 = sim.load_fitness(ic50_path)
    
n_doses = const_dose.shape
for dose in const_dose:

    counts = np.zeros((n_gen+1,ic50.shape[0]))
    tic=time.time()
    for sim_num in range(n_sims):
        counts_t, drug_curve = sim.var_fit_automaton(drugless_rates,
                                        ic50,
                                        n_gen=n_gen,  # Number of simulated generations
                                        mut_rate=mut_rate,  # probability of mutation per generation
                                        max_cells=max_cells,  # Max number of cells
                                        death_rate=death_rate,  # Death rate
                                        init_counts=init_counts,
                                        carrying_cap=carrying_cap,
                                        plot=plot,
                                        curve_type=curve_type,
                                        const_dose=dose,
                                        slope=slope,
                                        max_dose=max_dose,
                                        min_dose=min_dose,
                                        h_step=h_step)
        counts += counts_t
        
    toc=time.time()
    print('Elapsed time: ' + str(toc-tic))
    counts=np.divide(counts,n_sims)
    sim.plot_timecourse(counts,drug_curve,log_scale=log_scale)