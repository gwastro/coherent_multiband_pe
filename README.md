### (this repo is under construction)

## Multiband parameter estimation with phase coherence and extrinsic marginalization: Extracting more information from low-SNR CBC signals in LISA data

Shichao Wu 1,∗ Alexander H. Nitz 2,† Ian Harry 3, Stanislav Babak 4,
Michael J. Williams 3, Collin Capano 2,5, and Connor Weaving

$^1$ Max-Planck-Institut f{\"u}r Gravitationsphysik (Albert-Einstein-Institut) and Leibniz Universit{\"a}t Hannover, D-30167 Hannover, Germany
$^2$ Department of Physics, Syracuse University, Syracuse NY 13244, USA
$^3$ University of Portsmouth, Institute of Cosmology and Gravitation, Portsmouth PO1 3FX, United Kingdom
$^4$ Astroparticule et Cosmologie, Université de Paris, CNRS, 75013 Paris, France
$^5$ Department of Physics, University of Massachusetts Dartmouth, North Dartmouth, MA 02747, USA

This paper presents a novel coherent multiband analysis framework for characterizing stellar- and intermediate-mass binary black holes using LISA and next-generation ground-based detectors (ET and CE), leveraging the latest developments in the PyCBC pipeline. Given the population parameters inferred from LVK results and LISA's sensitivity limits at high frequencies, most stellar-mass binary black holes would likely have SNRs below 5 in LISA, but the most state-of-the-art multiband parameter estimation methods, such as those using ET and CE posteriors as priors for LISA, typically struggle to analyze sources with a LISA SNR less than 5. We present a novel coherent multiband parameter estimation method that directly calculates a joint likelihood, which is highly efficient; this efficiency is enabled by multiband marginalization of the extrinsic parameter space, implemented using importance sampling, which can work robustly even when the LISA SNR is as low as 3. Having an SNR of $\sim 3$ allows LISA to contribute nearly double the number of multiband sources. Even if LISA only observes for one year, most of the multiband detector-frame chirp mass's 90\% credible interval (less than $10^{-4} \mathrm{M}_\odot$) is still better than that of the most accurately measured events for ET+2CE network in 7.5 years of observation, by at least one order of magnitude. For the first time, we show efficient multiband Bayesian parameter estimation results on the population scale, which paves the way for large-scale astrophysical tests using multibanding. 
