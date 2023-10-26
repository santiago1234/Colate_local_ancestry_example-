library(relater)
library(dplyr)
library(readr)

coal <- read.coal('output.coal')

coal %>%
  group_by(epoch.start, group1, group2) %>% 
  summarize(mean = mean(haploid.coalescence.rate, na.rm = T), 
            lower = quantile(haploid.coalescence.rate, prob = 0.025, na.rm = T), 
            upper = quantile(haploid.coalescence.rate, prob = 0.975, na.rm = T)) -> coal


 coal %>% 
   write_csv('output-coals.csv')
 
 
