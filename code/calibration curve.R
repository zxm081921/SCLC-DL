library(survival)
library(rms) 
library(officer)
library(rvg)
read.table("PFSOStrain.csv",header = T,sep=",")->a
head(a)


library(tidyr) #调用units函数

units(a$OStime)<- "Month"#将时间指定为月，否则默认的是天数

dd=datadist(a)
options(datadist="dd")

coxm1<-cph(Surv(OStime,OSstatus==1)~ OSstrong,
           x=T,y=T,data=a,surv=T,time.inc = 12)
coxm2<-cph(Surv(OStime,OSstatus==1)~ OSstrong,
           x=T,y=T,data=a,surv=T,time.inc = 24)
coxm3<-cph(Surv(OStime,OSstatus==1)~ OSstrong,
           x=T,y=T,data=a,surv=T,time.inc = 36)

cal1<-calibrate(coxm1,cmethod='KM',method='boot',u=12,m=100,B=100)
cal1
cal2<-calibrate(coxm2,cmethod='KM',method='boot',u=24,m=100,B=100)
cal3<-calibrate(coxm3,cmethod='KM',method='boot',u=36,m=100,B=100)

plot(cal1,lwd=2,lty=1, 
     errbar.col="red", 
     xlim = c(0,1),ylim =c(0,1), 
     xlab="Predicted Probability of PFS",
     ylab="Actual Probability",
     subtitles=F, 
     col="red") 

plot(cal2,lwd=2,lty=1, 
     errbar.col="blue", 
     xlim = c(0,1),ylim =c(0,1), 
     xlab="Predicted Probability of PFS",
     ylab="Actual Probability",
     subtitles=F, 
     col="blue",add=TRUE) 

plot(cal3,lwd=2,lty=1, 
     errbar.col="green", 
     xlim = c(0,1),ylim =c(0,1), 
     xlab="Predicted Probability of PFS",
     ylab="Actual Probability",
     subtitles=F, 
     col="green",add=TRUE) 

abline(0,1,lty=3,lwd=2,col="black") 
legend("bottomright", c("6-months", "12-months", "18-months"), 
       col=c("red", "blue","green"), lty=1, lwd=2) 


