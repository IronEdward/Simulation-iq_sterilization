# Comparing populational IQ between sterilization under various thresholds
Rough simulation of the effects of sterilization on average populational IQ.
* Population
    * Start with 1000
    * 50/50 male/female ratio
    * Initial individual IQ follows Gaussian distribution
    * Individuals can die for various reasons
    * People die at 

* Marriage
    * 50% chance to marry for each step
    * Divorce/remarriage not considered
    * Parent-child relationship not considered

* Reproduction
    * 50% chance to have children
    * In sterilization mode, couples under a threshold IQ cannot have children
    * IQ of child is calculated by randoIQFromGaussianDistribution * 0.6 + femaleIQ * 0.3 + maleIQ * 0.1

* Generations
    * Step through 100 years (parameterizable)
    * Calculate average IQ and distribution for each step (visualization)

## Datasets/Sources
* http://www.ipss.go.jp/p-toukei/JMD/00/STATS/bltper_1x1.txt
* https://ourworldindata.org/marriages-and-divorces
* https://www.independent.co.uk/news/science/children-intelligence-iq-mother-inherit-inheritance-genetics-genes-a7345596.html