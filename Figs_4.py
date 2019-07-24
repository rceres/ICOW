# island City On a Wedge, a modeling framework of intermediate complexity

# Copyright (C) 2019 Robert L. Ceres

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

# Code used in this archive was used to develop all figures in Ceres, Forest, Keller, 2019.

import sys
method=sys.argv[1]
print(method)
dO=20
epss=0.05
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
outputPath='./ICOW/'
figPath=outputPath + 'figs/'

method=sys.argv[1]
if (method=="NSGAII"):
    sampledFutures=int(sys.argv[2])
    psize = int(sys.argv[3])
    iterations = int(sys.argv[4])
    fnamebase = outputPath + method + '_S_' + str(sampledFutures) + '_P_' + str(psize) + '_I_'+str(iterations)

if (method=="NSGAIII"):
    sampledFutures=int(sys.argv[2])
    dO=int(sys.argv[3])
    fnamebase =outputPath +  method + '_S_' + str(sampledFutures) + '_DO_'+str(dO)

if (method=="MOEAD"):
    sampledFutures=int(sys.argv[2])
    psize = int(sys.argv[3])
    fnamebase = outputPath + method  + '_S_' + str(sampledFutures) + '_P_' + str(psize)

if (method=="EpsMOEA"):
    sampledFutures=int(sys.argv[2])
    epss = float(ys.argv[3])
    fnamebase = outputPath + method + '_S_' + str(sampledFutures) + '_e_' + str(epss)

if (method=="BorgMOEA"):
    sampledFutures=int(sys.argv[2])
    psize = int(sys.argv[3])
    epss = float(sys.argv[4])
    nfe = int(sys.argv[5])
    id = str(sys.argv[6])
    fnamebase = outputPath + method + id

print('file name base')
print(fnamebase)

print('output path')
print(outputPath)

print('figure path')
print(figPath)
# Lables

resistance = "resistance (m)"
RH = "resistance (m)"
RP = "resistance percent (%)"
WH = "withdrawal (m)"
DB = "dike base (m)"
DH = "dike (m)"
r='R (m)'
p='P (percent)'
w='W (m)'
b='B (m)'
d='D(m)'
RPD = 0.5
WHD = 0
totalDamage = "tot damage ($)"
floodEvents = "flood events (#)"
breechEvents = "breech events (#)"
thresholdEvents = "threshold events (#)"
investmentCost = "investment cost ($)"
totalCost = "total cost ($)"
cityValueChange = "city value change ($)"
staveoffTime = "staveoff time (y)"

netCost = "net cost ($)"
instanceDamage = "damage ($)"
instanceNet = "net ($)"
openSpace = "undeveloped waterfront (m)"
dcost = "dike cost ($)"
rcost = 'resistance cost ($)'
wcost = 'withdrawal cost ($)'
damage = "damage cost ($)"
access = "accessible to waterfront (m)"

dollarUnitlabel = ' billion'
dollarUnit = 1000000000
investlabel='Investment cost'
netlabel = 'Net cost'
damagelabel = 'Damages'
DHlabel = 'Dike height'
RHlabel = 'Resistance height'
WHlabel = 'Withdrawal height'
RPlabel = 'Resistance percent'
DBlabel = 'Dike base'
investAxlabel=investlabel + ' ($' + dollarUnitlabel + ')'
netAxlabel = netlabel + ' ($' + dollarUnitlabel + ')'
damageAxlabel = damagelabel + ' ($' + dollarUnitlabel + ')'
DHAxlabel = DHlabel + ' (m)'
RHAxlabel = RHlabel + ' (m)'
WHAxlabel = WHlabel + ' (m)'
RPAxlabel = RPlabel + ' (%)'
DBAxlable = DBlabel + ' (m)'



investLim=100000e6/dollarUnit
netCostLim=80000e6/dollarUnit
damageLim=8000e7/dollarUnit
investLim2=3200e6/dollarUnit
investLim3=3200e7/dollarUnit

#from pyborg import BorgMOEA
from rhodium import *
from rhodium.ffi import NativeModel
#from pyborg import BorgMOEA
import matplotlib.pyplot as plt
import matplotlib.pylab

model_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")

model_DH.parameters = [Parameter(RH, default_value=100.0, type="double"),
                       Parameter(RP, default_value=RPD,type="double"),
                       Parameter(WH, default_value=100.0,type="double"),
                       Parameter(DB, default_value=100.0, type="double"),
                       Parameter(DH, default_value=100.0,type="double"),
                       Parameter("years", default_value=50,type="int"),
                       Parameter("sampled futures", default_value=sampledFutures,type="int")
                       ]

model_DH.responses = [Response(totalDamage, Response.MINIMIZE, type="double", asarg=True),
                      #Response(floodEvents, Response.INFO, type="double", asarg=True),
                      #Response(breechEvents, Response.INFO, type="double", asarg=True),
                      #Response(thresholdEvents, Response.INFO, type="double", asarg=True),
                      Response(investmentCost, Response.MINIMIZE, type="double", asarg=True),
                      #Response(totalCost, Response.MINIMIZE, type="double", asarg=True),
                      #Response(cityValueChange, Response.MAXIMIZE, type="double", asarg=True),
                      Response(netCost, Response.INFO, type="double", asarg=True),
                      Response(dcost, Response.INFO, type="double", asarg=True),                      
                      Response(rcost, Response.INFO, type="double", asarg=True),
                      Response(damage, Response.INFO, type="double", asarg=True),
                      Response(wcost, Response.INFO, type="double",assarg=False)
                      #Response(staveoffTime, Response.MAXIMIZE, type="double", asarg=True),
                      #Response(instanceDamage, Response.INFO, type="double", asarg=True),
                      #Response(instanceNet, Response.INFO, type="double", asarg=False)
                      ]

model_DH.levers = [RealLever(DH,0.0,18)]

model_RH= NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH.parameters = model_DH.parameters
model_RH.responses = model_DH.responses
model_RH.levers = [RealLever(RH, 0.0, 18)]


model_WH= NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_WH.parameters = model_DH.parameters
model_WH.responses = model_DH.responses
model_WH.levers = [RealLever(WH, 0.0, 18)]

model_RH_RP = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP.parameters = model_DH.parameters
model_RH_RP.responses = model_DH.responses
model_RH_RP.levers = [RealLever(RH,0.0,18), RealLever(RP,0.1,0.95)]

model_RH_RP_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_DH.parameters = model_DH.parameters
model_RH_RP_DH.responses = model_DH.responses
model_RH_RP_DH.levers = [RealLever(RH,0.0,18), RealLever(RP,0.1,0.95), RealLever(DH,0,18)]

model_RH_RP_WH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_WH.parameters = model_DH.parameters
model_RH_RP_WH.responses = model_DH.responses
model_RH_RP_WH.levers = [RealLever(RH,0.0,18), RealLever(RP,0.1,0.95), RealLever(WH,0,18)]

model_RH_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_DH.parameters = model_DH.parameters
model_RH_DH.responses = model_DH.responses
model_RH_DH.levers = [RealLever(RH,0.0,18),RealLever(DH, 0.0, 18)]

model_RH_DB_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_DB_DH.parameters = model_DH.parameters
model_RH_DB_DH.responses = model_DH.responses
model_RH_DB_DH.levers = [RealLever(RH, 0.0, 18),RealLever(DB, 0, 18),RealLever(DH, 0, 18)]
ts1=time.time()

model_WH_DB_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_WH_DB_DH.parameters = model_DH.parameters
model_WH_DB_DH.responses = model_DH.responses
model_WH_DB_DH.levers = [RealLever(WH, 0.0, 5.0),RealLever(DB, 0, 18),RealLever(DH, 0, 18)]

model_RH_RP_DB_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_DB_DH.parameters = model_DH.parameters
model_RH_RP_DB_DH.responses = model_DH.responses
model_RH_RP_DB_DH.levers = [RealLever(RH, 0.0, 18),RealLever(RP, 0.1, .95),RealLever(DB, 0.0, 18),RealLever(DH, 0, 18)]

model_RH_RP_WH_DB_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_WH_DB_DH.parameters = model_DH.parameters
model_RH_RP_WH_DB_DH.responses = model_DH.responses
model_RH_RP_WH_DB_DH.levers = [RealLever(RH, 0.0, 18),RealLever(RP, 0.1, .95),RealLever(WH, 0,18),RealLever(DB, 0.0, 18),RealLever(DH, 0, 18)]

print("starting " +  fnamebase + "_output_DH.json")
_, output_DH = load( fnamebase + "_output_DH.json")


#print(output_DH)
print("finished " + fnamebase + "_output_DH.json")

print("starting " + fnamebase + "_output_RH.json")
_, output_RH = load( fnamebase + "_output_RH.json")
#print(output_RH)
print("finished " + fnamebase + "_output_RH.json")

print("starting "+ fnamebase + "_output_WH.json")
_, output_WH = load( fnamebase + "_output_WH.json")
#print(output_WH)
print("finished " + fnamebase + "_output_WH.json")


print("starting " + fnamebase + "_output_RH_RP.json")
_, output_RH_RP = load( fnamebase + "_output_RH_RP.json")
#print(output_RH_RP)
print("finished " + fnamebase + "_output_RH_RP.json")

print("starting " + fnamebase + "_output_RH_DH.json")
_, output_RH_DH = load( fnamebase + "_output_RH_DH.json")
#print(output_RH_DH)
print("finished " + fnamebase + "_output_RH_DH.json")

print("starting " + fnamebase + "_output_RH_DB_DH.json")
_, output_RH_DB_DH = load( fnamebase + "_output_RH_DB_DH.json")
#print(output_RH_DB_DH)
print("finished " + fnamebase + "_output_RH_DB_DH.json")

print("starting " + fnamebase + "_output_WH_DB_DH.json")
_, output_WH_DB_DH = load( fnamebase + "_output_WH_DB_DH.json")
#print(output_RH_DB_DH)
print("finished " + fnamebase + "_output_WH_DB_DH.json")

print("starting " +  fnamebase + "_output_RH_RP_DB_DH.json")
_, output_RH_RP_DB_DH = load( fnamebase + "_output_RH_RP_DB_DH.json")

#print(output_RH_RP_DB_DH)
print("finished " + fnamebase + "_output_RH_RP_DB_DH.json")

print("starting " + fnamebase + "_output_RH_RP_WH_DB_DH.json")
_, output_RH_RP_WH_DB_DH = load( fnamebase + "_output_RH_RP_WH_DB_DH.json")
#print(output_RH_RP_WH_DB_DH)
print("finished " + fnamebase + "_output_RH_RP_WH_DB_DH.json")

print('convert to dataframes')
df_DH=output_DH.as_dataframe()
df_DH=df_DH.sort_values(investmentCost)
#print(df_DH)

df_RH=output_RH.as_dataframe()
df_RH=df_RH.sort_values(investmentCost)


df_WH=output_WH.as_dataframe()
df_WH=df_WH.sort_values(investmentCost)
#print(df_WH)

df_RH_RP=output_RH_RP.as_dataframe()
df_RH_RP=df_RH_RP.sort_values(investmentCost)


df_RH_DH=output_RH_DH.as_dataframe()
df_RH_DH=df_RH_DH.sort_values(investmentCost)


df_RH_DB_DH=output_RH_DB_DH.as_dataframe()
df_RH_DB_DH=df_RH_DB_DH.sort_values(investmentCost)
#print(df_RH_DB_DH)

df_WH_DB_DH=output_WH_DB_DH.as_dataframe()
df_WH_DB_DH=df_WH_DB_DH.sort_values(investmentCost)
#print(df_RH_DB_DH)

df_RH_RP_DB_DH=output_RH_RP_DB_DH.as_dataframe()
df_RH_RP_DB_DH=df_RH_RP_DB_DH.sort_values(investmentCost)


df_RH_RP_WH_DB_DH=output_RH_RP_WH_DB_DH.as_dataframe()
df_RH_RP_WH_DB_DH=df_RH_RP_WH_DB_DH.sort_values(investmentCost)


import matplotlib.patches as mpatches
import matplotlib.pyplot as plt




print('fig4')
lw=0.7
fig4=plt.figure(figsize=(10,7.5))
plt.subplot(3,2,1)
#f4a=plt.plot(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue', marker='None',linewidth=lw, label=None)
f4a=plt.scatter(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue',s=12, marker='.', label=None)
#f4a=plt.plot(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue', marker='.',linestyle='None', label=None)
#plt.plot(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey', marker='None', linestyle='none', label=None)
plt.scatter(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey',s=13,marker='.', label=None)
handle_DH=mpatches.Patch(color='tab:gray',alpha=.5,label='Dike')
handle_DH_RH=mpatches.Patch(color='lightblue',alpha=.5,label='+ Fixed resistance(0.5)')
handle_DH_DB_RH_RP=mpatches.Patch(color='b',alpha=.5,label='+ Base + Variable resistance')
handle_DH_DB_WH_RH_RP=mpatches.Patch(color='y',alpha=.5,label='+ Withdrawal')
leg1=plt.legend(handles=[handle_DH,handle_DH_RH,handle_DH_DB_RH_RP,handle_DH_DB_WH_RH_RP],loc='upper right', shadow=False)
leg1.get_frame().set_linewidth(0.0)
#plt.xlabel(investAxlabel)
plt.ylabel(damageAxlabel)
plt.xlim(0,investLim)
plt.ylim(0,damageLim)
plt.scatter(0,0,marker='o',color='lightgreen',s=800)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title(' a)', loc='Left')


plt.subplot(3,2,3)
#f4b=plt.plot(df_RH_RP_DB_DH[investmentCost]/dollarUnit, df_RH_RP_DB_DH[totalDamage]/dollarUnit,c = 'b', marker='.', linestyle='None', label=None)
f4c=plt.scatter(df_RH_RP_DB_DH[investmentCost]/dollarUnit, df_RH_RP_DB_DH[totalDamage]/dollarUnit,c = 'b',s=11, marker='.', label=None)
#plt.plot(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue', marker='None',linewidth=lw, label=None)
plt.scatter(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue',s=12, marker='.', label=None)
#plt.plot(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey', marker='None', linestyle='-.', label=None)
plt.scatter(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey',s=13,marker='.', label=None)
#handle_DH=mpatches.Patch(color='tab:gray',label='Dike')
#handle_DH_RH=mpatches.Patch(color='lightblue',label='+ Fixed resistance(0.5)')
#handle_DH_DB_RH_RP=mpatches.Patch(color='b',label='+ Base + Variable resistance')
#handle_DH_DB_WH_RH_RP=mpatches.Patch(color='y',label='+ Withdrawal')
#leg1=plt.legend(handles=[handle_DH,handle_DH_RH,handle_DH_DB_RH_RP,handle_DH_DB_WH_RH_RP],loc='upper right', shadow=False)
#leg1.get_frame().set_linewidth(0.0)
#plt.xlabel(investAxlabel)
plt.ylabel(damageAxlabel)
plt.xlim(0,investLim)
plt.ylim(0,damageLim)
plt.scatter(0,0,marker='o',color='lightgreen',s=800)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title(' c)', loc='Left')


plt.subplot(3,2,5)
#f4c=plt.plot(df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit, df_RH_RP_WH_DB_DH[totalDamage]/dollarUnit,c = 'y', marker='.',linestyle='None',linewidth=0.5, label=None)
f4e=plt.scatter(df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit, df_RH_RP_WH_DB_DH[totalDamage]/dollarUnit,c = 'y', s=10, marker='.', label=None)
#plt.plot(df_RH_RP_DB_DH[investmentCost]/dollarUnit, df_RH_RP_DB_DH[totalDamage]/dollarUnit,c = 'b', marker='None', linewidth=lw, label=None)
plt.scatter(df_RH_RP_DB_DH[investmentCost]/dollarUnit, df_RH_RP_DB_DH[totalDamage]/dollarUnit,c = 'b',s=11, marker='.', label=None)
#plt.plot(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue', marker='None',linewidth=lw, label=None)
plt.scatter(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue',s=12, marker='.', label=None)
#plt.plot(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey', marker='None', linestyle='-.', label=None)
plt.scatter(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey',s=13,marker='.', label=None)
#leg1=plt.legend(handles=[handle_DH,handle_DH_RH,handle_DH_DB_RH_RP,handle_DH_DB_WH_RH_RP],loc='upper right', shadow=False)
#leg1.get_frame().set_linewidth(0.0)
#handle_DH=mpatches.Patch(color='tab:gray',label='Dike')
#handle_DH_RH=mpatches.Patch(color='lightblue',label='+ Fixed resistance(0.5)')
#handle_DH_DB_RH_RP=mpatches.Patch(color='b',label='+ Base + Variable resistance')
#handle_DH_DB_WH_RH_RP=mpatches.Patch(color='y',label='+ Withdrawal')
plt.xlabel(investAxlabel)
plt.ylabel(damageAxlabel)
plt.xlim(0,investLim)
plt.ylim(0,damageLim)
plt.scatter(0,0,marker='o',color='lightgreen',s=800)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title(' e)', loc='Left')

plt.subplot(3,2,2)
handle_Dike=mpatches.Patch(color='grey',label='Dike')
handle_Fixed_Resistance=mpatches.Patch(color='lightblue',label='Fixed resistance')
handle_Resistance=mpatches.Patch(color='b',label='Variable resistance               ')
handle_Withdrawal=mpatches.Patch(color='y',label='Withdrawal')
x1 = df_RH_DB_DH[investmentCost]/dollarUnit
x2 = df_RH_DB_DH[investmentCost]/dollarUnit-df_RH_DB_DH[dcost]/dollarUnit
dFraction= df_RH_DB_DH[dcost]/df_RH_DB_DH[investmentCost]
rFraction= df_RH_DB_DH[rcost]/df_RH_DB_DH[investmentCost]

f4b=plt.fill_between(x1, 0.0, dFraction, color='grey', alpha='0.5')
plt.fill_between(x1,dFraction,dFraction+rFraction, color='lightblue', alpha='0.5')
#leg=plt.legend(handles=[handle_Dike, handle_Fixed_Resistance,handle_Resistance,handle_Withdrawal],loc='upper right', shadow=False)
#leg.get_frame().set_linewidth(0.0)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title(' b)', loc='Left')
#plt.xlabel(investAxlabel)
plt.ylabel('Fractional contribution')
plt.xlim(0,investLim)
plt.ylim(0,1)


x1 = df_RH_RP_DB_DH[investmentCost]/dollarUnit
x2 = df_RH_RP_DB_DH[investmentCost]/dollarUnit-df_RH_RP_DB_DH[dcost]/dollarUnit
dFraction= df_RH_RP_DB_DH[dcost]/df_RH_RP_DB_DH[investmentCost]
rFraction= df_RH_RP_DB_DH[rcost]/df_RH_RP_DB_DH[investmentCost]
plt.subplot(3,2,4)
f4d=plt.fill_between(x1, 0.0, dFraction, color='grey', alpha='0.5')
plt.fill_between(x1,dFraction,dFraction+rFraction, color='blue', alpha='0.5')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title(' d)', loc='Left')
#plt.xlabel(investAxlabel)
plt.ylabel('Fractional contribution')
plt.xlim(0,investLim)
plt.ylim(0,1)


x1 = df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit
x2 = df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit-df_RH_DB_DH[dcost]/dollarUnit
x3 = df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit-df_RH_DB_DH[dcost]/dollarUnit--df_RH_DB_DH[rcost]
dFraction=df_RH_RP_WH_DB_DH[dcost]/df_RH_RP_WH_DB_DH[investmentCost]
rFraction=df_RH_RP_WH_DB_DH[rcost]/df_RH_RP_WH_DB_DH[investmentCost]
wFraction=df_RH_RP_WH_DB_DH[wcost]/df_RH_RP_WH_DB_DH[investmentCost]
plt.subplot(3,2,6)
f4f=plt.fill_between(x1, 0.0, dFraction, color='grey', alpha='0.5')
plt.fill_between(x1,dFraction,dFraction+rFraction, color='blue', alpha='0.5')
plt.fill_between(x1,dFraction+rFraction, dFraction+rFraction+wFraction,color='yellow', alpha='0.5')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title(' f)', loc='Left')
plt.xlabel(investAxlabel)
plt.ylabel('Fractional contribution')
plt.xlim(0,investLim)
plt.ylim(0,1)


fig4.savefig((figPath + method + 'fig_4.pdf'),figsize=(16,10),bbox_inches='tight')
plt.show(fig4)

