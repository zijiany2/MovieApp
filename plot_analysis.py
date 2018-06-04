from analysis import Network
from math import log10
import matplotlib.pyplot as plt

if __name__ == "__main__":
    net = Network()
    # Plot Top 10 actors with most connections
    hub_10 = net.get_hub_actors(10)
    names, degrees = zip(*hub_10)
    plt.figure(1)
    x = range(10)
    plt.xticks(x, names, rotation=30)
    plt.bar(x, degrees, align='center', alpha=0.5)
    plt.xlabel('Actors')
    plt.ylabel('Number of connections')
    plt.title('Top 10 actors with most connections')
    plt.show()
    # Plot Age-Average gross in linear scale
    age_gross = net.get_age_average_gross_pairs()
    age = list(age_gross.keys())
    gross = list(age_gross.values())
    plt.figure(2)
    plt.scatter(age, gross)
    plt.xlim(xmin=-1, xmax=100)
    plt.xlabel('Age')
    plt.ylabel('Average gross')
    plt.title('Age-Average gross in linear scale')
    plt.show()
    # Plot Age-Average gross in log scale
    plt.figure(3)
    log_gross = [log10(y+1) for y in gross]
    plt.scatter(age, log_gross)
    plt.xlim(xmin=-1, xmax=100)
    plt.xlabel('Age')
    plt.ylabel('Average gross (power of 10)')
    plt.title('Age-Average gross in log scale')
    plt.show()
