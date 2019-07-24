import sys
method=sys.argv[1]
print(method)
dO=20
epss=0.05

outputPath='/home/scrim/rlc299/scratch/ICOW/'
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
df_DH=df_DH.sort_values(dcost)
print(df_DH)


