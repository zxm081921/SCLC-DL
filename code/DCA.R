# install.packages("devtools")
library(devtools)
devtools::install_github('yikeshu0611/ggDCA')
library("ggDCA")
library(rms)
library(survival)


rm(list = ls())

a<- read.csv('PFSOStest.csv')
head(a)
bb<-datadist(a)
options(datadist='bb')

model1<-coxph(Surv(OStime,OSstatus==1)~stage + chemotherapy1 + PCI, data=a)
model2<-coxph(Surv(OStime,OSstatus==1)~OSstrong, data=a)
model3<-coxph(Surv(OStime,OSstatus==1)~stage + chemotherapy0 + PCI + OSstrong, data=a)


dca<- dca(model1,model2,model3,
          times=6)

dca1<- dca(model1,model2,model3)


ggplot(dca1,linetype =F,
       lwd = 1.1)  

