# library(iterators,lib="~/lib64/R/library")
# library(foreach,lib="~/lib64/R/library")
# library(doMC,lib="~/lib64/R/library")
# library(Lmoments,lib="~/lib64/R/library")
# library(distillery,lib="~/lib64/R/library")
# install.packages('car',dependencies='Depends',lib="~/lib64/R/library")
# library(car,lib="~/lib64/R/library")
# library(extRemes,lib="~/lib64/R/library")
library(doMC)
library(extRemes)
registerDoMC(16)

GenerateABMArray<-function(observationruns,cases,years,TimeAdjustmentFactor,
                           LocationParam, LocationParamDeltaVector,
                           ScaleParam,ScaleParamDeltaVector,
                           ShapeParam,ShapeParamDeltaVector,RampPeriod,CaseVector)
{
  ABMSimVector<-unlist(foreach(i=1:years) %dopar%
                         {
                           foo<-unlist(foreach(j=1:cases) %do%
                                         {
                                           fo<-unlist(revd(observationruns,
                                                           loc=(LocationParam+DeltaLocationVector[i]*CaseVector[j]),
                                                           scale=(ScaleParam+DeltaScaleVector[i]*CaseVector[j]),
                                                           shape=ShapeParam))
                                           return(fo)
                                           } #%do%
                                       ) #foreach(j=1:cases)
                           return(foo)
                           } #%dopar%
                       )
  ABMSimArray<-array(data=ABMSimVector,dim=c(observationruns,cases,years))
  return(ABMSimArray) #unlist
} #function


SiteName<-'TheBattery'
returntimescale<-100 
RampPeriod<-100 # number of years that the ramp function takes to implement the full increase in surge value
LocationParam<- 0.9355858# New London value 0.8001887
ScaleParam<- 0.2055583 # New London value 0.1993277
ShapeParam<- 0.2326272 # New London value 0.128718
DeltaLocation<- 1
DeltaScale<-0.12143
DeltaShape<- 0
observationruns <- 10000000#10000000
years<-200
cases<-1

subname<-paste(SiteName, 'Ramped_DeltaLoc_',DeltaLocation,'DeltaScale_',DeltaScale,'DeltaShape_',DeltaShape,'obs_runs_',observationruns,collapse='_')
baselinetimeframe50position<-5   # RL calculated every 10 years. number corresponds to years*10 of initial observations
baselinetimeframe100position<-10 # RL calculated every 10 years. number corresponds to years*10 of initial observations
decadesobservations<-years/10
q<-0.95 #desired confidence of detection
CaseVector<-c(1.0)
t<-seq(from=0, to=(2*DeltaLocation),length.out=(years+1))[-1]
DeltaLocationVector<-c(t[1:40],rep(t[40],40),t[41:80],rep(t[80],40),t[81:120])
LocationVector<-DeltaLocationVector+LocationParam
t<-seq(from=0, to=(2*DeltaScale),length.out=(years+1))[-1]
DeltaScaleVector<-c(rep(0,40),t[1:40],rep(t[40],40),t[41:80],rep(t[80],40))
ScaleVector<-DeltaScaleVector+ScaleParam

ShapeParamDeltaVector<-c(0,0,DeltaShape*1,DeltaShape*1.85,DeltaShape*2.5,DeltaShape*3.0)
fname<-paste('~/scratch/ICOW',observationruns,Sys.Date(), sep = "_",colapse=NULL)

#################################################################
# Create the Array of Annual Block Maximums over all cases, over 
# all simulation runs. dimensions of ABMSimArray are 
# dim=c(observationruns,cases,years)
#################################################################

# LocationParamVector<-seq(from=LocationParam, to=(LocationParam+DeltaLocation*2),length.out=years)
# ScaleParamVector<-seq(from=ScaleParam, to=ScaleParam+DeltaScale,length.out=years)
DeltaShapeVector<-rep(0,200)


ABMSimArray<-GenerateABMArray(observationruns,cases,years,TimeAdjustmentFactor,LocationParam, DeltaLocationVector,
                              ScaleParam,DeltaScaleVector,ShapeParam,DeltaShapeVector,RampPeriod,CaseVector)
# #################################################################
# #Calculate return levels for each 200 year time series.
# # Standard case where initial estimates for Location, Scale, and
# # Shape parameters are not known.
# #################################################################
fname1<-paste(fname,"1", ".RData", sep = "",colapse=NULL)
save.image(file=fname1)



