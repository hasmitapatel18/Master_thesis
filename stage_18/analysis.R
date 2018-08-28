
rm(list=ls()) # clean up the workspace

# *******************************************************************
# Constructing priors on 'g' (genartion time) and
# 'u' (per-generation mutation rate)
# *******************************************************************



# generation prior construction
m <- 29.5; v <- (32-27)^2/16
a <- m^2/v; b <- m/v


# This is how the prior on 'g' looks like:
curve(dgamma(x, a, b), from=20, to=40, main="Distribution curve for the generation, g prior", xlab="Generation time, g (y)", ylab="Gamma(g | a, b)", las=1, n=5e2)

# mutation rate prior
# substitutions per site per 10^8 years.
m.r <- (1.36+0.97)/2; v.r <- (1.36-0.97)^2/16
a.r <- m.r^2/v.r; b.r <- m.r/v.r


# This is how the prior on 'u' looks like:
curve(dgamma(x, a.r, b.r), from=0, to= 2, main="Distribution curve for the mutation rate u prior", xlab="Per-generation mutation rate, u (x 10^-8)", ylab="Gamma(u | a, b)", las=1, n=5e2)

#import mcmc.txt file
m1 <- read.table("mcmc.txt", head=TRUE)  # contains 20,000 MCMC samples

names(m1)


# By using the priors on 'g' and 'u' we will convert the tau's into
# geological divergence times (in years) and the theta's into
# effective population sizes (as numbers of individuals)

# For example, this is how posterior distribution of the root's tau
# (age of the root in substitutions per site) looks like before
# re-calibrating it to geological time:
plot(density(m1$tau_10NeaDenYoruba_AFRSpain_EURChinese_EASPeru_AMRChimpGorOrang    ), xlim=c(0.0005,0.002), xlab="tau (in substitutions per site)", main="AFR/EUR Root tau")

# To obtain the calibrated times and population sizes, we simply
# obtain 20,000 samples from the priors on 'g' and 'u'.

# Recal that the per-yer mutation rate is r=u/g. Thus the calibrated
# times are t = tau/r. Also recall that theta = 4Nu, thus N = theta/(4u).
# So we simply use the sampled values of 'g' and 'u' to recalibrate all
# the tau's and theta's in the m1 dataframe:

n <- nrow(m1)  # 20,000
set.seed(123357)  # We set the set so that the analysis is reproducible
gi <- rgamma(n, a, b)               # sample from prior on 'g'
ri <- rgamma(n, a.r, b.r) * 1e-8    # sample from prior on 'u'

# Column indices for thau's and theta's
tau.i <- 10:17; theta.i <- 2:9

# Obtain population sizes (Ne) and geological times in years (ty):
Ne <- m1[,theta.i] / (4*ri)   # N = theta / (4*u)
ty <- m1[,tau.i] * gi / ri    # t = tau * g / u

# Voilá! Ne and ty contain our posterior estimates of population sizes
# and geological divergence times!

# For example, this is how the posterior distribution of the root's Ne
# and age look like:
plot(density(Ne$theta_10NeaDenYoruba_AFRSpain_EURChinese_EASPeru_AMRChimpGorOrang    , from=0, to=0.2e5), xlab = "Root's Ne (number of individuals)", main="Effective size of the root's ancestral population")
plot(density(ty$tau_10NeaDenYoruba_AFRSpain_EURChinese_EASPeru_AMRChimpGorOrang   /1e6, from=0, to=30e1), xlab = "Root's age (thousands of years ago)", main="Root age EAS/AM")

# Calculate posterior means and 95% credibility-intervals:
N.m <- apply(Ne, 2, mean)
N.95 <- apply(Ne, 2, quantile, prob=c(.025, .975))
t.m <- apply(ty, 2, mean)
t.95 <- apply(ty, 2, quantile, prob=c(.025, .975))

# print out a table of posterior means and CI's for Ne and ty for all
# the populations:
pop.names <- c("10NeaDenYoruba_AFRSpain_EURChinese_EASPeru_AMRChimpGorOrang", "11NeaDenYoruba_AFRSpain_EURChinese_EASPeru_AMRChimpGor", "12NeaDenYoruba_AFRSpain_EURChinese_EASPeru_AMRChimp", "13NeaDenYoruba_AFRSpain_EURChinese_EASPeru_AMR", "14NeaDen", "15Yoruba_AFRSpain_EURChinese_EASPeru_AMR", "16Spain_EURChinese_EASPeru_AMR", "17Chinese_EASPeru_AMR")
Ne.df <- cbind(N.m, t(N.95)); row.names(Ne.df) <-  pop.names
t.df <-  cbind(t.m, t(t.95)); row.names(t.df)  <-  pop.names
Ne.df; t.df
