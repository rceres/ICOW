# Copyright (C) 2017  Robert Ceres, Chris Forest, and Klaus Keller
# This program comes with ABSOLUTELY NO WARRANTY

# Software Author: Robert Ceres RobCeres@psu.edu

# This file is part of was used to used to conduct the OSSE experiments
# described in Ceres, Forest, Keller 2017, Understanding the detectability
# of potential changes to the 100-year peak storm surge published in 
# Climatic Change. This software is free: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

library(doMC)
cores<-1
registerDoMC(cores)
rm(list=ls())
load("ScaleNS_1e+05_2016-02-17_6.RData")
Surges<-ABMSimArray[,4,]
clippedSurges<-Surges
ramp<-seq(from = 12.01, by=0.01,length.out=200)

foreach(i=seq(1,200))%do%{
  clippedSurges[which(((Surges[,i]))>(ramp[i])),i]<-ramp[i]
}

write.csv(clippedSurges,file="surges.csv",row.names = FALSE,col.names=FALSE) 
SurgesFromFile<-read.csv(file="surges.csv")
dim(SurgesFromFile)