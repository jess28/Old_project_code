# Master's Project (Copy Number Variation)
This repository contains code from my Master's project. It is organized by language and then by whether it is specific to the project or a piece of utility code. You can find my thesis published on [Zenodo](https://zenodo.org/record/48371).

## So what's this about?
I needed to find large areas of [copy number variation](https://en.wikipedia.org/wiki/Copy-number_variation) within _Drosophila melanogaster_ sex-separated genomes. I needed to create code for every step in my process.
* Combining the many individual male and female sequences into one male and one female sequence
* Splitting the fly genome into equally sized windows and counting how many times something mapped to that area
* Determining the statistical differences between windows across sex, and within sex
* Creating visualizations of each chromosome's copy number variation

I used Python for the data manipulation: combining data sets together, creating equal splits along chromosomes, preparing the data for use in bioinformatic tools such as [BWA](http://bio-bwa.sourceforge.net/), [GATK](https://www.broadinstitute.org/gatk/), and [Samtools](http://www.htslib.org/). I used R for statistical analysis and visualization.
