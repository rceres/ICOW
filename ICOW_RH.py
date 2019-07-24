import sys
method=sys.argv[1]
print(method)
dO=20
dI=10
epss=0.05

outputPath='/home/scrim/rlc299/scratch/ICOW/'


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

print(fnamebase)
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
RPL = 0.4
RPD = 0.5
RPH = 0.999
DHL=0
DHH=18
RHL=0
RHH=16
WHL=0
WHH=5
DBL=0
DBH=10
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
investLim=6e10
netCostLim=8e10
damageLim=8e10

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
                      Response(investmentCost, Response.MINIMIZE, type="double", asarg=True),
                      Response(r, Response.INFO, type="double", asarg=True),
                      Response(b, Response.INFO, type="double",asarg=True),
                      Response(dcost, Response.INFO, type="double",asarg=True),
                      Response(rcost, Response.INFO, type="double",asarg=True),
                      Response(wcost, Response.INFO, type="double",asarg=False)
                      ]

model_DH.levers = [RealLever(DH, DHL, DHH)]

model_RH= NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH.parameters = model_DH.parameters
model_RH.responses = model_DH.responses
model_RH.levers = [RealLever(RH, RHL, RHH)]


model_WH= NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_WH.parameters = model_DH.parameters
model_WH.responses = model_DH.responses
model_WH.levers = [RealLever(WH, WHL, WHH)]

model_RH_RP = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP.parameters = model_DH.parameters
model_RH_RP.responses = model_DH.responses
model_RH_RP.levers = [RealLever(RH, RHL, RHH), RealLever(RP, RPL, RPH)]

model_RH_RP_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_DH.parameters = model_DH.parameters
model_RH_RP_DH.responses = model_DH.responses
model_RH_RP_DH.levers = [RealLever(RH, RHL, RHH), RealLever(RP, RPL,RPH), RealLever(DH, DHL, DHH)]

model_RH_RP_WH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_WH.parameters = model_DH.parameters
model_RH_RP_WH.responses = model_DH.responses
model_RH_RP_WH.levers = [RealLever(RH, RHL, RHH), RealLever(RP, RPL,RPH), RealLever(WH, WHL, WHH)]

model_RH_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_DH.parameters = model_DH.parameters
model_RH_DH.responses = model_DH.responses
model_RH_DH.levers = [RealLever(RH, RHL, RHH),RealLever(DH, DHL, DHH)]

model_RH_DB_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_DB_DH.parameters = model_DH.parameters
model_RH_DB_DH.responses = model_DH.responses
model_RH_DB_DH.levers = [RealLever(RH, RHL, RHH),RealLever(DB, DBL, DBH),RealLever(DH, DHL, DHH)]

model_WH_DB_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_WH_DB_DH.parameters = model_DH.parameters
model_WH_DB_DH.responses = model_DH.responses
model_WH_DB_DH.levers = [RealLever(WH, WHL, WHH),RealLever(DB, DBL, DBH),RealLever(DH, DHL, DHH)]

model_RH_RP_DB_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_DB_DH.parameters = model_DH.parameters
model_RH_RP_DB_DH.responses = model_DH.responses
model_RH_RP_DB_DH.levers = [RealLever(RH, RHL, RHH),RealLever(RP, RPL,RPH),RealLever(DB, DBL, DBH),RealLever(DH, DHL, DHH)]

model_RH_RP_WH_DB_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_WH_DB_DH.parameters = model_DH.parameters
model_RH_RP_WH_DB_DH.responses = model_DH.responses
model_RH_RP_WH_DB_DH.levers = [RealLever(RH, RHL, RHH),RealLever(RP, RPL,RPH),RealLever(WH, WHL, WHH),RealLever(DB, DBL, DBH),RealLever(DH, DHL, DHH)]


ts1=time.time()
print('starting RH')
if (method=="NSGAII"):
    output_RH = optimize(model_RH, method, iterations, population_size=psize)

if (method=="MOEAD"):
    output_RH = optimize(model_RH, method, population_size=psize)

if (method=="NSGAIII"):
    output_RH = optimize(model_RH, method, divisions_outer=dO)

if (method=="EpsMOEA"):
    output_RH=optimize(model_RH, method, epsilons=epss)

if (method=="BorgMOEA"):
    output_RH=optimize(model_RH, algorithm=method, module="pyborg", population_size=psize, epsilons=epss,NFE=10000)
    
ts2=time.time()
save(output_RH, fnamebase + "_output_RH.json")
print(ts2-ts1)
print(fnamebase)
