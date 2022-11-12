# innerlife: "Verbs of inner life"

Script to visualize the "inner life" data from ELTeC. 

## What does it do?

For each language represented in the dataset, produces 
- a scatterplot with a regression line, for all verbs jointly, per novel
- a boxplot, for all verbs jointly, summarized per decade 
- a comparison plot for the earlier vs. the later part of the data.
- the same series of plots for each category of verbs separately.
  
Some plots are skipped if (a) there is no data for a given category of verbs in a given language or (b) if, for the KDE plot, the sample size is smaller than 25 per group. 

## Known issues

- (2022-11-12) The KDE plots vary depending on the sample selected. Current solution: Create the KDE plot once, but calculate p-values 100 times and report average p-value and standard deviation. 
- (2022-11-12) Something strange is going on in the Hungarian dataset when calculating the KDE plots: for some samples, no p-value can be calculated, because the mean does not compute. 
- (2022-11-12) For some languages, there is insufficient data for a meaningful comparison between early and late period. 
- 2022-11-12 For nor, there are two errors in the metadata (year of publication is much later than 1920).  
