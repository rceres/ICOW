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
    dO=sys.argv[3]
    fnamebase =outputPath +  method + '_S_' + str(sampledFutures) + '_DO_'+str(dO)

if (method=="MOEAD"):
    sampledFutures=int(sys.argv[2])
    psize = sys.argv[3]
    fnamebase = outputPath + method  + '_S_' + str(sampledFutures) + '_P_' + str(psize)

if (method=="EpsMOEA"):
    sampledFutures=int(sys.argv[2])
    epss = sys.argv[3]
    fnamebase = outputPath + method + '_S_' + str(sampledFutures) + '_e_' + str(epss)

if (method=="BorgMOEA"):
    sampledFutures=int(sys.argv[2])
    psize = int(sys.argv[3])
    epss = float(sys.argv[4])
    nfe = int(sys.argv[5])
    fnamebase = outputPath + method + '_S_' + str(sampledFutures) + '_P_' + str(psize) + '_e_' + str(epss) + '_NFE_' + str(nfe)

print(fnamebase)
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

model_RH_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_DH.parameters = model_DH.parameters
model_RH_DH.responses = model_DH.responses
model_RH_DH.levers = [RealLever(RH,0.0,18),RealLever(DH, 0.0, 18)]

model_RH_DBH_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_DBH_DH.parameters = model_DH.parameters
model_RH_DBH_DH.responses = model_DH.responses
model_RH_DBH_DH.levers = [RealLever(RH, 0.0, 18),RealLever(DB, 0, 18),RealLever(DH, 0, 18)]
ts1=time.time()

model_RH_RP_DBH_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_DBH_DH.parameters = model_DH.parameters
model_RH_RP_DBH_DH.responses = model_DH.responses
model_RH_RP_DBH_DH.levers = [RealLever(RH, 0.0, 18),RealLever(RP, 0.1, .95),RealLever(DB, 0.0, 18),RealLever(DH, 0, 18)]

model_RH_RP_WH_DBH_DH = NativeModel("iCOW.dylib", "evaluateDamageOverTime")
model_RH_RP_WH_DBH_DH.parameters = model_DH.parameters
model_RH_RP_WH_DBH_DH.responses = model_DH.responses
model_RH_RP_WH_DBH_DH.levers = [RealLever(RH, 0.0, 18),RealLever(RP, 0.1, .95),RealLever(WH, 0,18),RealLever(DB, 0.0, 18),RealLever(DH, 0, 18)]

ts1=time.time()
print('starting DH')
# Optimize the model using Rhodium
if (method=="NSGAII"):
    output_DH = optimize(model_DH, method, iterations, population_size=psize)


if (method=="MOEAD"):
    output_DH = optimize(model_DH, method, population_size=psize)

if (method=="NSGAIII"):
    output_DH = optimize(model_DH, method, divisions_outer=dO)

if (method=="EpsMOEA"):
    output_DH=optimize(model_DH, method, epsilons=epss)

if (method=="BorgMOEA"):
    output_DH=optimize(model_DH, algorithm=method, module="pyborg", population_size=psize, epsilons=epss,NFE=10000)

print(fnamebase+"_output_DH.json")
ts2=time.time()
save(output_DH, fnamebase + "_output_DH.json")
#print(output_DH)
df_DH=output_DH.as_dataframe()

print('DH')
print(ts2-ts1)
t_DH=ts2-ts1

ts1=time.time()
print('starting RH')
# Optimize the model using Rhodium
if (method=="NSGAII"):
    output_RH = optimize(model_RH, method, iterations, population_size=psize)
    
if (method=="MOEAD"):
    output_RH = optimize(model_RH, method, population_size=psize)

if (method=="NSGAIII"):
    output_RH = optimize(model_RH, method, divisions_outer=dO)

if (method=="EpsMOEA"):
    output_RH=optimize(model_RH, method, epsilons=epss)

if (method=="BorgMOEA"):
    output_RH=optimize(model_RH, algorithm=method, module="pyborg", population_size=psize, epsilons=epss,NFE=nfe)

ts2=time.time()
save(output_RH,  fnamebase + "_output_RH.json")
df_RH=output_RH.as_dataframe()
#print(output_RH)
print('RH')
print(ts2-ts1)
t_RH=ts2-ts1

ts1=time.time()
print('starting WH')
# Optimize the model using Rhodium
if (method=="NSGAII"):
    output_WH = optimize(model_WH, method, iterations, population_size=psize)

if (method=="MOEAD"):
    output_WH = optimize(model_WH, method, population_size=psize)

if (method=="NSGAIII"):
    output_WH = optimize(model_WH, method, divisions_outer=dO)

if (method=="EpsMOEA"):
    output_WH=optimize(model_WH, method, epsilons=epss)

if (method=="BorgMOEA"):
    output_WH=optimize(model_WH, algorithm=method, module="pyborg", population_size=psize, epsilons=epss,NFE=10000)

ts2=time.time()
save(output_WH, fnamebase + "_output_WH.json")
df_WH=output_WH.as_dataframe()
print('WH')
print(ts2-ts1)
t_WH=ts2-ts1

ts1=time.time()
print('starting RH_RP')
# Optimize the model using Rhodium
if (method=="NSGAII"):
    output_RH_RP = optimize(model_RH_RP, method, iterations, population_size=psize)

if (method=="MOEAD"):
    output_RH_RP = optimize(model_RH_RP, method, population_size=psize)

if (method=="NSGAIII"):
    output_RH_RP = optimize(model_RH_RP, method, divisions_outer=dO)

if (method=="EpsMOEA"):
    output_RH_RP=optimize(model_RH_RP, method, epsilons=epss)

if (method=="BorgMOEA"):
    output_RH_RP=optimize(model_RH_RP, algorithm=method, module="pyborg", population_size=psize, epsilons=epss,NFE=10000)

ts2=time.time()
save(output_RH_RP, fnamebase + "_output_RH_RP.json")
df_RH_RP=output_RH_RP.as_dataframe()
print('RH_RP')
print(ts2-ts1)
t_RH_RP=ts2-ts1

ts1=time.time()
print('starting RH_DH')
# Optimize the model using Rhodium
if (method=="NSGAII"):
    output_RH_DH = optimize(model_RH_DH, method, iterations, population_size=psize)

if (method=="MOEAD"):
    output_RH_DH = optimize(model_RH_DH, method, population_size=psize)

if (method=="NSGAIII"):
    output_RH_DH = optimize(model_RH_DH, method, divisions_outer=dO)

if (method=="EpsMOEA"):
    output_RH_DH=optimize(model_RH_DH, method, epsilons=epss)

if (method=="BorgMOEA"):
    output_RH_DH=optimize(model_RH_DH, algorithm=method, module="pyborg", population_size=psize, epsilons=epss,NFE=10000)

ts2=time.time()
save(output_RH_DH, fnamebase + "_output_RH_DH.json")
df_RH_DH=output_RH_DH.as_dataframe()
t_RH_DH=ts2-ts1
print('RH_DH')
print(ts2-ts1)

ts1=time.time()
print('starting RH_DBH_DH')
# Optimize the model using Rhodium
if (method=="NSGAII"):
    output_RH_DBH_DH = optimize(model_RH_DBH_DH, method, iterations, population_size=psize)


if (method=="MOEAD"):
    output_RH_DBH_DH = optimize(model_RH_DBH_DH, method, population_size=psize)

if (method=="NSGAIII"):
    output_RH_DBH_DH = optimize(model_RH_DBH_DH, method, divisions_outer=dO)

if (method=="EpsMOEA"):
    output_RH_DBH_DH=optimize(model_RH_DBH_DH, method, epsilons=epss)

if (method=="BorgMOEA"):
    output_RH_DBH_DH=optimize(model_RH_DBH_DH, algorithm=method, module="pyborg", population_size=psize, epsilons=epss,NFE=10000)

ts2=time.time()
save(output_RH_DBH_DH, fnamebase + "_output_RH_DBH_DH.json")
df_RH_DBH_DH=output_RH_DBH_DH.as_dataframe()
t_RH_DBH_DH=ts2-ts1
print('RH_DBH_DH')
print(ts2-ts1)

ts1=time.time()
print('starting RH_RP_DBH_DH')
if (method=="NSGAII"):
    output_RH_RP_DBH_DH = optimize(model_RH_RP_DBH_DH, method, iterations, population_size=psize)

if (method=="MOEAD"):
    output_RH_RP_DBH_DH = optimize(model_RH_RP_DBH_DH, method, population_size=psize)

if (method=="NSGAIII"):
    output_RH_RP_DBH_DH = optimize(model_RH_RP_DBH_DH, method, divisions_outer=dO)

if (method=="EpsMOEA"):
    output_RH_RP_DBH_DH=optimize(model_RH_RP_DBH_DH, method, epsilons=epss)

if (method=="BorgMOEA"):
    output_RH_RP_DBH_DH=optimize(model_RH_RP_DBH_DH, algorithm=method, module="pyborg", population_size=psize, epsilons=epss,NFE=10000)

ts2=time.time()
save(output_RH_RP_DBH_DH, fnamebase + "_output_RH_RP_DBH_DH.json")
#print(output_RH_RP_DBH_DH)
df_RH_RP_DBH_DH=output_RH_RP_DBH_DH.as_dataframe()
t_RH_RP_DBH_DH=ts2-ts1
print('RH_RP_DBH_DH')
print(ts2-ts1)

ts1=time.time()
print('starting RH_RP_WH_DBH_DH')
if (method=="NSGAII"):
    output_RH_RP_WH_DBH_DH = optimize(model_RH_RP_WH_DBH_DH, method, iterations, population_size=psize)

if (method=="MOEAD"):
    output_RH_RP_WH_DBH_DH = optimize(model_RH_RP_WH_DBH_DH, method, population_size=psize)

if (method=="NSGAIII"):
    output_RH_RP_WH_DBH_DH = optimize(model_RH_RP_WH_DBH_DH, method, divisions_outer=dO)


if (method=="EpsMOEA"):
    output_RH_RP_WH_DBH_DH=optimize(model_RH_RP_WH_DBH_DH, method, epsilons=epss)

if (method=="BorgMOEA"):
    output_RH_RP_WH_DBH_DH=optimize(model_RH_RP_WH_DBH_DH, algorithm=method, module="pyborg", population_size=psize, epsilons=epss,NFE=10000)

ts2=time.time()
print(ts2-ts1)
t_RH_RP_WH_DBH_DH=ts2-ts1
#print(output_RH_RP_WH_DBH_DH)
save(output_RH_RP_WH_DBH_DH, fnamebase + "_output_RH_RP_WH_DBH_DH.json")
df_RH_RP_WH_DBH_DH=output_RH_RP_WH_DBH_DH.as_dataframe()
t_RH_RP_WH_DBH_DH=ts2-ts1
print('RH_RP_WH_DBH_DH')
print(ts2-ts1)


print('t_DH')
print(t_DH)
print('t_RH')
print(t_RH)
print('t_WH')
print(t_WH)
print('t_RH_RP')
print(t_RH_RP)
print('t_RH_DH')
print(t_RH_DH)
print('t_RH_DBH_DH')
print(t_RH_DBH_DH)
print('t_RH_RP_DBH_DH')
print(t_RH_RP_DBH_DH)
print('t_RH_RP_WH_DBH_DH')
print(t_RH_RP_WH_DBH_DH)
print(fnamebase)
