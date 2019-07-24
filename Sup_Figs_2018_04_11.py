import json
import sys
from rhodium import *
from rhodium.ffi import NativeModel
import matplotlib.pyplot as plt
import matplotlib.pylab
method='BorgMOEA'

outputPath='./ICOW/'
figPath=outputPath + 'figs/'

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



investLim=1100e9/dollarUnit
netCostLim=400e9/dollarUnit
damageLim=300e9/dollarUnit
investLim2=400e9/dollarUnit
investLim3=600e9/dollarUnit

import matplotlib.pyplot as plt
import matplotlib.pylab

print("loading output files")

a='BorgMOEAstates_'
b='_1000K__output_RH_RP_WH_DB_DH.json'
f=outputPath+a+'1'+b
print(f)
_, F = load(f)
df00001=F.as_dataframe()
df00001=df00001.sort_values(investmentCost)

f=outputPath+a+"2"+b
print(f)
_, F = load(str(f))
df00002=F.as_dataframe()
df00002=df00002.sort_values(investmentCost)

f=outputPath+a+"10"+b
print(f)
_, F = load(f)
df00010=F.as_dataframe()
df00010=df00010.sort_values(investmentCost)

f=outputPath+a+"20"+b
print(f)
_, F = load(f)
df00020=F.as_dataframe()
df00020=df00020.sort_values(investmentCost)

f=outputPath+a+"50"+b
print(f)
_, F = load(f)
df00050=F.as_dataframe()
df00050=df00050.sort_values(investmentCost)

f=outputPath+a+"100"+b
print(f)
_, F = load(f)
df00100=F.as_dataframe()
df00100=df00100.sort_values(investmentCost)

f=outputPath+a+"200"+b
print(f)
_, F = load(f)
df00200=F.as_dataframe()
df00200=df00200.sort_values(investmentCost)

f=outputPath+a+"500"+b
print(f)
_, F = load(f)
df00500=F.as_dataframe()
df00500=df00500.sort_values(investmentCost)

f=outputPath+a+"1000"+b
print(f)
_, F = load(f)
df01000=F.as_dataframe()
df01000=df01000.sort_values(investmentCost)

f=outputPath+a+"2000"+b
print(f)
_, F = load(f)
df02000=F.as_dataframe()
df02000=df02000.sort_values(investmentCost)

f=outputPath+a+"5000"+b
print(f)
_, F = load(f)
df05000=F.as_dataframe()
df05000=df05000.sort_values(investmentCost)

f=outputPath+a+"10000"+b
print(f)
_, F = load(f)
df10000=F.as_dataframe()
df10000=df10000.sort_values(investmentCost)

f=outputPath+a+"20000"+b
print(f)
_, F = load(f)
df20000=F.as_dataframe()
df20000=df20000.sort_values(investmentCost)


import matplotlib.patches as mpatches
import matplotlib.pyplot as plt



print('fig S2 Increasing Futures')
figS2=plt.figure()
fS2=plt.plot(df00001[investmentCost]/dollarUnit,df00001[netCost]/dollarUnit,color='c',marker='.',linestyle='-.',label='    1 future',linewidth=0.5)
plt.plot(df00010[investmentCost]/dollarUnit,df00010[netCost]/dollarUnit,color='m',marker='.',linestyle='-.',label='   10 futures',linewidth=0.5)
plt.plot(df00100[investmentCost]/dollarUnit,df00100[netCost]/dollarUnit,color='y',marker='.',linestyle='-.',label='  100 futures',linewidth=0.5)
plt.plot(df00200[investmentCost]/dollarUnit,df00200[netCost]/dollarUnit,color='grey',marker='.',linestyle='-.',label='  200 futures',linewidth=0.5)
#plt.plot(df00500[investmentCost]/dollarUnit,df00500[netCost]/dollarUnit,color='blue',marker='.',linestyle='-.',label='500 futures',linewidth=0.5)
plt.plot(df01000[investmentCost]/dollarUnit,df01000[netCost]/dollarUnit,color='k',marker='.',linestyle='-.',label=' 1000 futures',linewidth=0.5)
#plt.plot(df02000[investmentCost]/dollarUnit,df02000[netCost]/dollarUnit,color='b',marker='.',linestyle='-.',label=' 2000 futures',linewidth=0.5)
#plt.plot(df05000[investmentCost]/dollarUnit,df05000[netCost]/dollarUnit,color='r',marker='.',linestyle='-.',label=' 5000 futures',linewidth=0.5)
plt.plot(df10000[investmentCost]/dollarUnit,df10000[netCost]/dollarUnit,color='g',marker='.',linestyle='-.',label='10000 futures',linewidth=0.5)



plt.xlabel('Costs ($ billion)')
plt.ylabel('Costs ($ billion)')
plt.xlim(0,investLim/3)
plt.ylim(0,investLim/3)
plt.legend(loc='upper right', shadow=False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title('S1)', loc='Left')
figS2.savefig((figPath + method + 'fig_S2.pdf'),bbox_inches='tight')
#plt.show(f1_S1a_vanDantzig_DH)

plt.show(fS2)

