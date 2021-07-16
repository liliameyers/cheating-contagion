# import modules
import matplotlib.pyplot as plt

def main():
    pass


def evaluation_plot(actual_motif_count, simulated_motif_count):
    '''Takes two inputs: 1) an integer representing the actual
    motif count and 2) a list of simulated motif counts. 
    Returns a plot showing the number of observer-cheater 
    motifs observed in the actual data (using a vertical line) 
    compared to the distribution from the randomized data
    (using a histogram).'''
            
    # set figure, axes size
    fig, ax = plt.subplots(figsize = (8, 5.5))
    
    # plot histogram of simulated motifs 
    plt.hist(x = simulated_motif_count,\
             bins = len(simulated_motif_count),\
             color = 'lightblue',\
             edgecolor = 'k',\
             label = "Simulated")
    
    # plot vertical line of actual motifs
    plt.axvline(x = actual_motif_count,\
                color = 'red',\
                linewidth = 2.5,\
                linestyle = '--',\
                label = "Actual")
    
    # add legend below plot
    plt.legend(loc = "lower center",\
               bbox_to_anchor = (0.5, -0.25),\
               ncol = 2)
    
    # add title and axes labels
    plt.title('Number of observer-cheater motifs in PUBG:\n Actual vs. Simulated',\
             fontsize = 13)
    plt.xlabel('Number of observer-cheater motifs', fontsize = 11)
    plt.ylabel('Frequency', fontsize = 11)
    
    # show plot
    plt.show()
    
    
if __name__ == '__main__':
    main()
