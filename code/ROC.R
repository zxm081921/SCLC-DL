read.table("PFSOStest.csv",header = T,sep=",")->a
head(a)
# install.packages("timeROC",type="binary")
library(timeROC)
library(survival)


  plot(timeROC(T=a$PFStime, #结局时间 
               delta=a$PFSstatus, #结局指标 
               marker=a$combined0, #预测变量 
               cause=1, #阳性结局指标数值 
               times=c(12), ROC=TRUE),time=12, col="red") 

  legend("bottomright", c("1-year"), 
         col=c("red"), lty=1, lwd=2) #添加标签信息