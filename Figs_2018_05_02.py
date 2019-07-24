import sys
method=sys.argv[1]
print(method)
dO=20
dI=10
epss=0.05

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

dollarUnitlabel = ' million'
dollarUnit = 1000000
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



investLim=11000e6/dollarUnit
netCostLim=400e6/dollarUnit
damageLim=1000e7/dollarUnit
investLim2=400e6/dollarUnit
investLim3=750e7/dollarUnit

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



print('fig S1 van Dantzig')
figS1a_vanDantzig_DH=plt.figure()
f1_S1a_vanDantzig_DH=plt.plot(df_DH[DH],df_DH[investmentCost]/dollarUnit,color='c',marker='.',linestyle='-.',label=investlabel,linewidth=0.5)
plt.xlabel(DHAxlabel)
plt.ylabel('Costs ($ million)')
plt.xlim(0,14)
plt.ylim(0,netCostLim)
#plt.scatter(x=dollarUnit,y=dollarUnit,marker='o',color='m',s=800)
plt.plot(df_DH[DH],df_DH[totalDamage]/dollarUnit,color='grey',marker='.',linestyle=':',label=damagelabel,linewidth=0.5)
plt.plot(df_DH[DH], df_DH[netCost]/dollarUnit,c = 'k',marker='.',linestyle='--',label=netlabel,linewidth=0.5)
plt.legend(loc='upper right', shadow=False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title('S1)', loc='Left')
figS1a_vanDantzig_DH.savefig((figPath + method + 'fig_S1a.pdf'),bbox_inches='tight')
#plt.show(f1_S1a_vanDantzig_DH)

print('fig3')
fig3=plt.figure()

handle_DH=mpatches.Patch(color='tab:gray',label='Dike')
handle_DH_RH=mpatches.Patch(color='c',label='+ Resistance')
handle_DH_DB_RH=mpatches.Patch(color='lightblue',label='+ Resistance & Base Height')
handle_DH_DB_RH_RP=mpatches.Patch(color='b',label='+ Reistance %')
handle_DH_DB_WH_RH_RP=mpatches.Patch(color='y',label='+ Withdrawal')
plt.subplot(2,3,1)
f3a=plt.plot(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue', marker='None',linewidth=0.5, label=None)
plt.scatter(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue',s=12, marker='.', label=None)
plt.plot(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey', marker='None', linestyle='-.', label=None)
plt.scatter(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey',s=13,marker='.', label=None)
plt.legend(handles=[handle_DH,handle_DH_DB_RH],loc='upper right', shadow=False)
#plt.xlabel(investAxlabel)
plt.ylabel(damageAxlabel)
plt.xlim(0,investLim2)
plt.ylim(0,damageLim)
plt.scatter(0,0,marker='o',color='lightgreen',s=800)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)

print('fig4')
lw=0.7
fig4=plt.figure(figsize=(10,7.5))
plt.subplot(3,2,1)
f4a=plt.plot(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue', marker='None',linewidth=lw, label=None)
plt.scatter(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue',s=12, marker='.', label=None)
plt.plot(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey', marker='None', linestyle='-.', label=None)
plt.scatter(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey',s=13,marker='.', label=None)
handle_DH=mpatches.Patch(color='tab:gray',label='Dike')
handle_DH_RH=mpatches.Patch(color='lightblue',label='+ Fixed resistance(0.5)')
handle_DH_DB_RH_RP=mpatches.Patch(color='b',label='+ Base + Variable resistance')
handle_DH_DB_WH_RH_RP=mpatches.Patch(color='y',label='+ Withdrawal')
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
f4b=plt.plot(df_RH_RP_DB_DH[investmentCost]/dollarUnit, df_RH_RP_DB_DH[totalDamage]/dollarUnit,c = 'b', marker='None', linewidth=lw, label=None)
plt.scatter(df_RH_RP_DB_DH[investmentCost]/dollarUnit, df_RH_RP_DB_DH[totalDamage]/dollarUnit,c = 'b',s=11, marker='.', label=None)
plt.plot(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue', marker='None',linewidth=lw, label=None)
plt.scatter(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue',s=12, marker='.', label=None)
plt.plot(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey', marker='None', linestyle='-.', label=None)
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
f4c=plt.plot(df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit, df_RH_RP_WH_DB_DH[totalDamage]/dollarUnit,c = 'y', marker='None',linestyle='-',linewidth=0.5, label=None)
plt.scatter(df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit, df_RH_RP_WH_DB_DH[totalDamage]/dollarUnit,c = 'y', s=10, marker='.', label=None)
plt.plot(df_RH_RP_DB_DH[investmentCost]/dollarUnit, df_RH_RP_DB_DH[totalDamage]/dollarUnit,c = 'b', marker='None', linewidth=lw, label=None)
plt.scatter(df_RH_RP_DB_DH[investmentCost]/dollarUnit, df_RH_RP_DB_DH[totalDamage]/dollarUnit,c = 'b',s=11, marker='.', label=None)
plt.plot(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue', marker='None',linewidth=lw, label=None)
plt.scatter(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue',s=12, marker='.', label=None)
plt.plot(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey', marker='None', linestyle='-.', label=None)
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

f4d=plt.fill_between(x1, 0.0, dFraction, color='grey', alpha='0.8')
plt.fill_between(x1,dFraction,dFraction+rFraction, color='lightblue', alpha='0.8')
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
f4e=plt.fill_between(x1, 0.0, dFraction, color='grey', alpha='0.8')
plt.fill_between(x1,dFraction,dFraction+rFraction, color='blue', alpha='0.6')
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
f4f=plt.fill_between(x1, 0.0, dFraction, color='grey', alpha='0.8')
plt.fill_between(x1,dFraction,dFraction+rFraction, color='blue', alpha='0.6')
plt.fill_between(x1,dFraction+rFraction, dFraction+rFraction+wFraction,color='yellow', alpha='0.5')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title(' f)', loc='Left')
plt.xlabel(investAxlabel)
plt.ylabel('Fractional contribution')
plt.xlim(0,investLim)
plt.ylim(0,1)


fig4.savefig((figPath + method + 'fig_4.pdf'),figsize=(16,10),bbox_inches='tight')
#plt.show(fig4)

print('fig5')
handle_Dike=mpatches.Patch(color='grey',label='Dike top')
handle_Resistance=mpatches.Patch(color='b',label='Resistance')
handle_Withdrawal=mpatches.Patch(color='y',label='Withdrawal')
handle_Dike_Base=mpatches.Patch(color='lightgrey',label='Dike base')
fig5=plt.figure()
f5=plt.scatter(df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit, df_RH_RP_WH_DB_DH[WH]+df_RH_RP_WH_DB_DH[DB]+df_RH_RP_WH_DB_DH[DH],c = 'grey',marker='+',s=10, label=None)
plt.scatter(df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit, df_RH_RP_WH_DB_DH[WH]+df_RH_RP_WH_DB_DH[RH],c = 'b',marker='+',s=(10*df_RH_RP_WH_DB_DH[RP]), label=None)
plt.plot(df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit, df_RH_RP_WH_DB_DH[WH],c = 'y',marker=None,linestyle='-',linewidth=1, label=None)
plt.scatter(df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit, df_RH_RP_WH_DB_DH[WH]+df_RH_RP_WH_DB_DH[DB],c = 'lightgrey',marker='.',s=10, label=None)

leg2=plt.legend(handles=[handle_Dike, handle_Resistance, handle_Withdrawal,handle_Dike_Base],loc='right', shadow=False)
leg2.get_frame().set_linewidth(0.0)
plt.xlabel(investAxlabel)
plt.ylabel("City elevation (m)")
plt.xlim(0,investLim)
plt.ylim(0,16)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
#plt.title('4)', loc='Left')
fig5.savefig((figPath + method + 'fig_5.pdf'),bbox_inches='tight')


figS4=plt.figure()
fS4=plt.plot(df_DH[investmentCost]/dollarUnit, df_DH[totalDamage]/dollarUnit,c = 'grey', marker=None,linestyle='-',linewidth=1.2,label='DH')
plt.plot(df_RH[investmentCost]/dollarUnit, df_RH[totalDamage]/dollarUnit,c = 'lightgreen',marker=None,linestyle='-',linewidth=.5,label='RH')
plt.plot(df_WH[investmentCost]/dollarUnit, df_WH[totalDamage]/dollarUnit,c = 'orange',marker=None,linestyle='-',linewidth=1.2,label='WH')
plt.plot(df_RH_RP[investmentCost]/dollarUnit, df_RH_RP[totalDamage]/dollarUnit,c = 'darkgreen',marker=None,linestyle='-',linewidth=1.2,label='RH + R%')
plt.plot(df_RH_RP_WH_DB_DH[investmentCost]/dollarUnit, df_RH_RP_WH_DB_DH[totalDamage]/dollarUnit,c = 'y', marker=None,linestyle='-',linewidth=.5,label='DH + DB, + RH + R% + WH')
plt.plot(df_RH_RP_DB_DH[investmentCost]/dollarUnit, df_RH_RP_DB_DH[totalDamage]/dollarUnit,c = 'blue', marker=None,linestyle='-',linewidth=.5,label='DH + DB, + RH + R%')
plt.plot(df_WH_DB_DH[investmentCost]/dollarUnit, df_WH_DB_DH[totalDamage]/dollarUnit,c = 'orange', marker=None,linestyle='-',linewidth=.5,label='DH + DB, + WH')
plt.plot(df_RH_DB_DH[investmentCost]/dollarUnit, df_RH_DB_DH[totalDamage]/dollarUnit,c = 'lightblue',marker=None,linestyle='-',linewidth=.5,label='DH + DB + RH')
plt.plot(df_RH_DH[investmentCost]/dollarUnit, df_RH_DH[totalDamage]/dollarUnit,c = 'magenta',marker=None,linestyle='-',linewidth=.5,label='DH + RH')


plt.xlabel(investAxlabel)
plt.ylabel(damageAxlabel)
plt.xlim(0,investLim)
plt.ylim(0,damageLim)
plt.scatter(0,0,marker='o',color='lightgreen',s=800)
plt.legend(loc='upper right', shadow=False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title('S4)', loc='Left')
#figS4.savefig((figPath + method + 'fig_S4.pdf'),bbox_inches='tight')



from rhodium import *
from rhodium.ffi import NativeModel
sns.set()
sns.set_style("white",)
sns.set_context("paper")

#figS6=plt.figure()
fS6=scatter2d(model_RH_RP_WH_DB_DH,output_RH_RP_WH_DB_DH,x=investmentCost,y=RH,c=RP,show_legend=True)
plt.xlabel(investAxlabel)
plt.ylabel('Resistance height (m)')
plt.title('S6)',loc='Left')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
fS6.savefig((figPath + method + 'fig_S6.pdf'),bbox_inches='tight')



f6=scatter3d(model_RH_RP_WH_DB_DH, output_RH_RP_WH_DB_DH, x=DH, y=WH, z=RH, s=DB, c=RP, show_legend=True,linestyle=':',linewidth=0.5)
#plt.title('5)',loc='Left')
f6.savefig((figPath + method + '_'+id + '_'+ 'fig_6.pdf'),bbox_inches='tight')
plt.show(f6)

print(figPath + figPath)
mpl.rcdefaults()
