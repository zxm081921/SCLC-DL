library(foreign)
library(rms) 
library(officer)
library(rvg)
read.table("PFSOStrain.csv",header = T,sep=",")->a
head(a)

dd=datadist(a)
options(datadist="dd") 

coxm<-cph(Surv(OStime,OSstatus==1)~stage + chemotherapy1 + PCI + OSstrong,x=T,y=T,data=a,surv=T)
surv<-Survival(coxm)
surv1<-function(x)surv(12,lp=x)
surv2<-function(x)surv(24,lp=x)
surv3<-function(x)surv(36,lp=x)

nom<-nomogram(coxm,fun=list(surv1,surv2,surv3),lp=F,
              funlabel = c("1-year Survival","2-year Survival",
                           "3-year Survival"),maxscale = 100,
              fun.at=c('0.99','0.9','0.8','0.7','0.5','0.3','0.1','0.01'))

plot((nom),xfrac=.3) 

