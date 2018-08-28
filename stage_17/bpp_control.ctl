seed =  -1

seqfile = /Users/hasmitapatel/Desktop/codedapes.txt
Imapfile = Imap.txt
outfile = /Users/hasmitapatel/Desktop/block_creation/output/output.txt
mcmcfile = /Users/hasmitapatel/Desktop/block_creation/output/mcmc.txt

speciesdelimitation = 0 * fixed species tree
*  speciesdelimitation = 1 0 2    * speciesdelimitation algorithm0 and finetune(e)
*  speciesdelimitation = 1 1 2 1  * speciesdelimitation algorithm1 finetune (a m)

species&tree = 9  Yoruba_AFR  Spain_EUR  Chinese_EAS  Peru_AMR  Nea  Den  Chimp  Gor  Orang
                  1           1          1            1         1    1    1      1    1
       (((((Nea, Den), (Yoruba_AFR,(Spain_EUR, (Chinese_EAS, Peru_AMR)))), Chimp), Gor), Orang);


usedata = 1    * 0: no data (prior); 1:seq like
nloci = 14663    * number of data sets in seqfile

cleandata = 0    * remove sites with ambiguity data (1:yes, 0:no)?

thetaprior =  2 2000   # gamma(a, b) for theta
tauprior = 14 1000   # gamma(a, b) for root tau & Dirichlet(a) for other tau's

*     locusrate = 0 2.0   # (0: No variation, 1: estimate, 2: from file) & a_Dirichlet (if 1)
*      heredity = 0 4 4   # (0: No variation, 1: estimate, 2: from file) & a_gamma b_gamma (if 1)
* sequenceerror = 0 0 0 0 : 0.05 1   # sequencing errors: a_gamma, b_gamma

*       finetune = 0: 0.5 0.002 0.0006  0.0004 0.06 0.2 1.0  # auto (0 or 1): finetune for GBtj, GBspr, theta, tau, mix, locusrate, seqerr

finetune = 1: .01 .01 .01 .01 .01 .01 .01 .01  # auto (0 or 1): finetune for GBtj, GBspr, theta, tau, mix, locusrate, seqerr

print = 1 0 0 0   * MCMC samples, locusrate, heredityscalars Genetrees
burnin = 2000
sampfreq = 2
nsample = 20000

*** Note: Make your window wider (140 columns) before running the program.
