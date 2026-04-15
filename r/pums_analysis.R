setwd("/home/ajchi/personal-projects/r-and-stuff")
library(data.table)
library(survey)

cols_needed <- c("AGEP", "SCHL", "FOD1P", "ESR", "PWGTP", "WAGP")

pums_a <- fread("psam_pusa.csv", select = cols_needed)
pums_b <- fread("psam_pusb.csv", select = cols_needed)
pums <- rbind(pums_a, pums_b)

#FOD1P: 2102 = CS, 2407 = CE
#SCHL: 21 = Bachelors, 22 = Masters 
#ESR: 1 = Employed at work, 2 = Employed but not at work, 3 = Unemployed (does not include those not in labor force)
cs_grads <- pums[
  AGEP >= 22 & AGEP <= 27 &
  FOD1P %in% c("2407") &
  SCHL %in% c("21", "22") &
  ESR %in% c("1", "2", "3")
]

# How many people aged 22-27 total3
#nrow(pums[AGEP >= 22 & AGEP <= 27])

# How many of those have a bachelor's or master's
#nrow(pums[AGEP >= 22 & AGEP <= 27 & SCHL %in% c("21", "22")])

# How many of those are CS
#nrow(pums[AGEP >= 22 & AGEP <= 27 & 
#            SCHL %in% c("21", "22") & 
#            (FOD1P %in% c("2102"))])

table(cs_grads$SCHL, cs_grads$ESR)

contingency_table <- table(cs_grads$SCHL, cs_grads$ESR)
chisq.test(contingency_table)

#adding new ESR_collapsed column: "employed if ESR is 1 or 2 else "unemployed"
cs_grads$ESR_collapsed <- ifelse(cs_grads$ESR %in% c("1", "2"), "employed", "unemployed")
chisq.test(table(cs_grads$SCHL, cs_grads$ESR_collapsed))$expected

# Define the survey design object with the weights
cs_survey <- svydesign(ids = ~1, weights = ~PWGTP, data = cs_grads)

# Weighted chi-square test
svychisq(~SCHL + ESR_collapsed, design = cs_survey, statistic = "Chisq")

# Weighted unemployment rates by degree level
#svyby(~I(ESR == "3"), ~SCHL, design = cs_survey, svymean)

#T test for difference in wages between BS and CS students
cs_employed <- cs_grads[ESR_collapsed == "employed"]
cs_employed$SCHL <- droplevels(factor(cs_employed$SCHL))
cs_employed_survey <- svydesign(ids = ~1, weights = ~PWGTP, data = cs_employed)
svyttest(WAGP ~ SCHL, design = cs_employed_survey)

#figuring out if CS or CE majors make more


