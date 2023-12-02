read.table("PFSOSvalidation.csv",header = T,sep=",")->a
head(a)
library(survminer)
library(survival)
library(officer)
library(rvg)


km.plot <- ggsurvplot(survfit(Surv(OStime,OSstatus)~ clinical, data = a),
                      pval = TRUE, 
                      conf.int = TRUE,   # 或conf.int = F则为不显示置信区间
                      risk.table = TRUE,
                      palette = c("#E7B800", "#2E9FDF"))

