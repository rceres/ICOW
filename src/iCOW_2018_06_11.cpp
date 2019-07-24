//
//  main.cpp
//  ICOW
//
//  Created by Robert Ceres on 11/9/17.
//  Copyright © 2017 Robert Ceres. All rights reserved.
//

#include <iostream>
#include <stdio.h>
#include <math.h>
#include <vector>
#include <fstream>
#include <sstream>
#include <chrono>
#include <random>
#include<algorithm>

using namespace std;

extern "C" {
  const double resistanceAdjustment=1.25;
    const double CEC=17;              //m City Elevation Change, Bennet Park in the Washington Heights area of Manhattan is 
    const double CityWidth=43000.0;                      //m
    const double CityLength=2000.0;                     //m
    const double CitySlope=CityLength/CityWidth;
    const double TotalCityValueInitial = 1500000000000; // 1,500,000,000,000 1,000,000,000,000  1,00,000,000,000;  50,000,000,000,000
    const double WithdrawelPercentLost = 0.01;
    const double BH = 30;//20; //m
    const double ProtectedValueRatio = 1.1;
    const double SlopeDike = .5;
    const double DikeUnprotectedValuationRatio = 0.95;
    const double WidthDikeTop = 3; //m
    const double DikeStartingCostPoint = 2;
    const double UnitCostPerVolumeDike = 10; //$ dollars per m^3

    const double WithdrawelCostFactor = 1.0;
    const double resistanceExponentialFactor = 0.115;
    const double resistanceLinearFactor=0.35;//0.45;
    const double resistanceExponentialThreshold = .4;
    const double damageFactor = 0.39;
    // i.e. damage is worse when the dike fails
    const double FailedDikeDamageFactor = 1.5; // considers additional damage that resutls because of dike failure
    const double intactDikeDamageFactor = 0.03;
    const double pfThreshold=0.95;
    const double pfBase=.05;
    const double minHeight=.1;
    const double Basement=3.0;    
    const double threshold = TotalCityValueInitial/375;
    const double thresholdDamageFraction = 1.0;
    // threhold is a demarcation of damage that is considered unacceptable
    // thresholdDamageFraction = 0 causes damage to accumulate at the normal (below threshold) rate
    // threshioldDamageMultiple = 1 causes damage to accululate at normal + normal (2x) below threshold rate
    const double thresholdDamageExponent = 1.01;

    const int lengthSurgeSequences=200;
   
    const double baseValue=100;
    const double PBase=0.5;
    const double Seawall=1.75;  // from Talke
    const double runUpWave=1.1; // to account for wave/runup. 1.0 results in no increase
    const int maxSurgeBlock=5000;

    
    // index lables for the city
    const int caseNum=0;
    const int wh=1;
    const int rh=2;
    const int rp=3;
    const int dbh=4;
    const int dh=5;
    const int vz1=6;
    const int vz2=7;
    const int vz3=8;
    const int vz4=9;
    const int tz1=10;
    const int tz2=11;
    const int tz3=12;
    const int tz4=13;
    const int fw=14;
    const int tcvi=15; // total city value initial
    const int ilfw=16;
    const int tcvaw=17;
    const int vifod=18;
    const int vbd=19;
    const int fcv=20;
    const int dc=21;
    const int wc=22;
    const int rc=23;
    const int tic=24; // total investment cost
    const int tc=25; // total net cost includes TIC plus loss of city value
    const int dtr=26;
    const int numCityChar=27;
    
    // index values for the damageVector
    const int dvt=0;  // total damage cost
    const int dvz1=1;  // damage zone 1
    const int dvz2=2;  // damage zone 2
    const int dvz3=3;  // damage zone 3
    const int dvz4=4;  // damage zone 4
    const int dvFE=5;  // Flood Event, some damage occurs
    const int dvBE=6;  // Breech Event
    const int dvTE=7;  // Threshold Event
    const int dvLength=8;

    
    double CalculateDikeCost(double hd,double cd,double S,double W,double sd,double wdt,double ich){
        // hd height of dike
        // cd cost of dike per unit volume
        // S slope of ground
        // W width of dike
        // sd slope of the dike sides
        // wdt width of the top of the dike
        // ich initial cost height
        double result;
        
        
        double ch;  /* Cost height is the dike height plus the equivalent height for startup costs. */
        double ch2; /* Cost height squared, used a lot, so calculate it once */
        double ld;  /* length of dike is height of dike divided by slope of the ground */
        double ld2; /* squared length of the dike is used alot, so calculate it once */
        double a22; /* an approximate side length, see paper for details */
        double a42; /* an approximate side length, see paper for details */
        double vd;  /* volume of dike */
        ch=hd+ich;
        ch2=pow(ch,2);
        ld=ch/S;
        //vd=W*ch*(wdt+ch/sd/2)+ld*ch*wdt+
        //sqrt(ch2*ld2*(a22+ld2+a42-ch2)+a22*ld2*(ch2+ld2+a42-a22)+ld2*a42*(ch2+a22+ld2-a42)-
        //     ch2*a22*a42-a22*ld2*ld2-ch2*ld2*ld2-a42*ld2*ld2)/6 ;
        vd=W*ch*(wdt+ch/pow(sd,2))+
              pow((
                -pow(ch,4)*pow((ch+1/sd),2)/pow(sd,2)-
                2*(pow(ch,5)*(ch+1/sd))/pow(S,4)-
                4*pow(ch,6)/(pow(sd,2)*pow(S,4))+
                4*pow(ch,4)*(2*dh*(ch+1/sd)-4*ch2+ch2/pow(sd,2))/(pow(sd,2)*pow(S,2))+
                2*pow(ch,3)*(ch+1/sd)/pow(S,2)
                ),1/2)/6+
              W*(ch2/pow(S,2));
        // volume of front of dike + volume of straight part of two sides of dike + volume tetrahedron part of sides */
        result=vd*cd;
        return result;
    }
    
    
    double CalculateWithdrawalCost(double * cityChar)
    // vi value of initial infrastructure
    // hw amount of height to withdraw to
    // h total height change of city
    // cw percent of value required to withdraw
    {
      double result;
      if (cityChar[wh]==0) result=0;
      else result=cityChar[tcvi]*cityChar[wh]/(CEC-cityChar[wh])*WithdrawelCostFactor;
      return(result);
    }
    
    double CalculateResiliencyCost1(double * cityChar){
        //dike base height is lower than resiliency height, there is an unprotected nonResiliant zone
        double fractionResilient=(Basement+cityChar[rh]/2) / BH;
 /*       double rcf = resistanceExponentialFactor *
        (cityChar[rp] +
         pow( (pow( cityChar[rp], RF2) +
               1) ,
             RF2) -
         1);*/
         double fcR = resistanceAdjustment*(resistanceExponentialFactor*std::max(0.0,(cityChar[rp]-resistanceExponentialThreshold))/(1.0-cityChar[rp]) +
                  cityChar[rp]*resistanceLinearFactor);
        return ( cityChar[vz1] * fcR * (fractionResilient));
    }
    
    //dike base height is lower than resiliency height, there is NOT an unprotected nonResiliant zone
    // cases 2 and 6
    double CalculateResiliencyCost2(double * cityChar){
        /*double rcf = resistanceExponentialFactor *
        (cityChar[rp] +
         pow( (pow( cityChar[rp], RF2) +
               1) ,
             RF2) -
         1);*/
         double fcR = resistanceAdjustment*(resistanceExponentialFactor*std::max(0.0,(cityChar[rp]-resistanceExponentialThreshold))/(1.0-cityChar[rp]) +
                  cityChar[rp]*resistanceLinearFactor);
        return( cityChar[vz1] * fcR * (Basement+cityChar[rh]-cityChar[dbh]/2) / BH);
    }
    
    double CalculateCostOfInfrastructureLostFromWithdrawal(double * cityChar)
    {
        
        //        return(cityChar[tcvi]*cityChar[fw]*WithdrawelPercentLost);
        return(cityChar[tcvi]*cityChar[fw]*WithdrawelPercentLost);
    }
    
    
    double CalculateFinalValueOfInfrastructure(double vi,double vil)
    // vi intial value of all infrastructure
    // vil value of infrastructure leaving
    {
        return(vi-vil);
    }
    
    
    double culateTotalCostAbatement(double cd,double cw,double cvlw,double cr)
    //   cd cost of dike
    //   cw cost of withdrawal
    //   cvlw cost of infrastructure lost due to withdrawal
    //   cr cost of resilancy
    {
        double result;
        result=cd+cw+cvlw+cr;
        return(result);
    }
    
    void CharacterizeCity (double W,double B,double R,double P, double D, double * cityChar) {

        // check for base value and strategies above min heights
        if (W==baseValue) {cityChar[wh]=0.0;} else {cityChar[wh]=W;}
        if (R==baseValue || R<minHeight) 
          {
            cityChar[rh]=0.0;
            cityChar[rp]=0.5;
          }
          else
          {
            cityChar[rh]=R;
            cityChar[rp]=P;
          }
        if (D==baseValue) {cityChar[dh]=0.0;} else {cityChar[dh]=D;}
        if (B<minHeight)
        {
            cityChar[dbh]=0.0;
            cityChar[rh]=0;
        }
        else
        {
          if (B==baseValue) 
          {
            cityChar[dbh]=0;
          }
          else 
          {
            cityChar[dbh]=B;
          }
        }
        
        // calculate the damage that results according to the resistance percent
        cityChar[dtr]=std::max(1-cityChar[rp],0.0);
        
        //check to see if the distance between top of withdrawal and dike base is too small
        if ((cityChar[dh]>=minHeight)&&(cityChar[dbh]<minHeight)&&(cityChar[rh]>=minHeight))
        {
          cityChar[dbh]=0;
          cityChar[rh]=0;
          }         
        int c=100; // which case?
        
        // (cityChar[dh]>0)
        if (cityChar[dh]>0) {
            
            // (cityChar[dh]>0) && (cityChar[dbh]>0)
            if (cityChar[dbh]>0) {
                
                // (cityChar[dh]>0) && (cityChar[dbh]>0) && (cityChar[rh]>0)
                if (cityChar[rh]>0) {
                    
                    // (cityChar[dh]>0) && (cityChar[dbh]>0) && (cityChar[rh]>0) && (cityChar[rh]<cityChar[dbh]) c=1
                    if (cityChar[rh]<cityChar[dbh]) {
                        c=1;
                    }
                    
                    // (cityChar[dh]>0) && (cityChar[dbh]>0) && (cityChar[rh]>0) && (cityChar[rh]>=cityChar[dbh]) c=2
                    else {
                        c=2;
                    }
                    
                }
                // (cityChar[dh]>0) && (cityChar[dbh]>0) && (cityChar[rh]=0) c=3
                else {
                    c=3;
                }
                
            }
            
            // (cityChar[dh]>0) && (cityChar[dbh]=0)
            else {
                c=4;             //there is a dike, there is no setback, there is or is not resilency
            }
        }
        
        // else (cityChar[dh]=0)
        else {
            if (cityChar[dbh]>0) {  // (cityChar[dh]=0) && (cityChar[dbh]>0)
                
                // if (cityChar[dh]=0) && (cityChar[dbh]>0) && (cityChar[rh]>0)
                if (cityChar[rh]>0) {
                    
                    // (cityChar[dh]=0) && (cityChar[dbh]>0) && (cityChar[rh]>0) && (cityChar[rh]<cityChar[dbh])
                    if (cityChar[rh]<cityChar[dbh]) {
                        c=5;  // no dike, but there is set back, and there is resiliency, resiliancy is lower than set back
                    }
                    // (cityChar[dh]=0) && (cityChar[dbh]>0) && (cityChar[rh]>0) && (cityChar[rh]>=cityChar[dbh])
                    else {
                        c=6;  // no dike, but there is set back, and there is resiliency, resiliancy is equal or higher than set back
                    }
                }
                // (cityChar[dh]=0) && (cityChar[dbh]>0) && (cityChar[rh]=0)
                else {
                    c=7;
                }
            }
            
            // (cityChar[dh]=0) && (cityChar[dbh]=0)
            else {
                
                // (cityChar[dh]=0) && (cityChar[dbh]=0) && (cityChar[rh]>0)
                if (cityChar[rh]>0) {
                    c=8;
                }
                // (cityChar[dh]=0) && (cityChar[dbh]=0) && (cityChar[rh]=0)
                else  {
                    c=9;
                }
            }
        }
        
        // implications of withdrawel are calculeted first since they will impact the rest of the calculations
        cityChar[tcvi]=TotalCityValueInitial;
        cityChar[wc]=CalculateWithdrawalCost(cityChar); //
        cityChar[fw]=cityChar[wh]/CEC; // Calculate Fraction Withdrawn
        cityChar[ilfw]=CalculateCostOfInfrastructureLostFromWithdrawal(cityChar);
        cityChar[tcvaw]=cityChar[tcvi]-cityChar[wc]; // calculate total city value after withdrawel
        cityChar[caseNum]=c;
        switch ( c ) {
            case 0:       // not valid
                break;
            case 1:        // (cityChar[dh]>0) && (cityChar[dbh]>0) && (cityChar[rh]>0) && (cityChar[rh]<cityChar[dbh])
                // city has all four zones
                
                cityChar[dc]=CalculateDikeCost(cityChar[dh],UnitCostPerVolumeDike,CitySlope,CityWidth,SlopeDike,WidthDikeTop,DikeStartingCostPoint);
                // and the dike is setback (cityChar[dbh]>0) and there is resiliency
                cityChar[vz1] = cityChar[tcvaw]*DikeUnprotectedValuationRatio*cityChar[rh]/(CEC-cityChar[wh]); // calculate value zone 1
                cityChar[vz2] = cityChar[tcvaw]*DikeUnprotectedValuationRatio*(cityChar[dbh]-cityChar[rh])/(CEC-cityChar[wh]); // calculate value zone 2
                cityChar[vz3] = cityChar[tcvaw]*ProtectedValueRatio*cityChar[dh]/(CEC-cityChar[wh]); // calculate value zone 3
                cityChar[vz4] = cityChar[tcvaw]*(CEC-cityChar[wh]-cityChar[dbh]-cityChar[dh])/(CEC-cityChar[wh]); // calculate value zone 4
                cityChar[fcv] = cityChar[vz1]+cityChar[vz2]+cityChar[vz3]+cityChar[vz4];
                cityChar[tz1] = cityChar[wh]+cityChar[rh];
                cityChar[tz2] = cityChar[wh]+cityChar[dbh];
                cityChar[tz3] = cityChar[wh]+cityChar[dbh]+cityChar[dh];
                cityChar[tz4] = CEC;
                cityChar[rc]  = CalculateResiliencyCost1(cityChar);
                cityChar[tic] = cityChar[wc]+cityChar[dc]+cityChar[rc];
                cityChar[tc]  = cityChar[tic]+cityChar[fcv]-cityChar[tcvi];
                break;
            case 2:         // (cityChar[dh]>0) && (cityChar[dbh]>0) && (cityChar[rh]>0) && (cityChar[rh]>=cityChar[dbh])
                cityChar[dc] = CalculateDikeCost(cityChar[dh],UnitCostPerVolumeDike,CitySlope,CityWidth,SlopeDike,WidthDikeTop,DikeStartingCostPoint);
                cityChar[vz1] = cityChar[tcvaw]*DikeUnprotectedValuationRatio*cityChar[dbh]/(CEC-cityChar[wh]); // calculate value zone 1
                cityChar[vz2] = 0; // there is no unprotected zone in front of the dike
                cityChar[vz3] = cityChar[tcvaw]*ProtectedValueRatio*cityChar[dh]/(CEC-cityChar[wh]); // calculate value zone 3
                cityChar[vz4] = cityChar[tcvaw]*(CEC-cityChar[wh]-cityChar[dbh]-cityChar[dh])/(CEC-cityChar[wh]); // calculate value zone 4
                cityChar[fcv] = cityChar[vz2]+cityChar[vz3]+cityChar[vz4];
                cityChar[tz1] = cityChar[wh]+cityChar[dbh];
                cityChar[tz2] = cityChar[wh]+cityChar[dbh];
                cityChar[tz3] = cityChar[wh]+cityChar[dbh]+cityChar[dh];
                cityChar[tz4] = CEC;
                cityChar[rc]  = CalculateResiliencyCost2(cityChar);
                cityChar[tic] = cityChar[wc]+cityChar[dc]+cityChar[rc];
                cityChar[tc]  = cityChar[tic]+cityChar[fcv]-cityChar[tcvi];
                break;
            case 3:        // (cityChar[dh]>0) && (cityChar[dbh]>0) && (cityChar[rh]=0)
                //the dike is not at the seawall and there is no resilancy
                cityChar[dc]  = CalculateDikeCost(cityChar[dh],UnitCostPerVolumeDike,CitySlope,CityWidth,SlopeDike,WidthDikeTop,DikeStartingCostPoint);
                cityChar[vz1] = 0; // not needed, we defined it this way
                cityChar[vz2] = cityChar[tcvaw]*DikeUnprotectedValuationRatio*cityChar[dbh]/(CEC-cityChar[wh]); // calculate value zone 2
                cityChar[vz3] = cityChar[tcvaw]*ProtectedValueRatio*cityChar[dh]/(CEC-cityChar[wh]); // calculate value zone 3
                cityChar[vz4] = cityChar[tcvaw]*(CEC-cityChar[wh]-cityChar[dbh]-cityChar[dh])/(CEC-cityChar[wh]); // calculate value zone 4
                cityChar[fcv] = cityChar[vz2]+cityChar[vz3]+cityChar[vz4];
                cityChar[tz1] = cityChar[wh];
                cityChar[tz2] = cityChar[wh]+cityChar[dbh];
                cityChar[tz3] = cityChar[wh]+cityChar[dbh]+cityChar[dh];
                cityChar[tz4] = CEC;
                cityChar[rc]  = 0; // there is no resiliency
                cityChar[tic] = cityChar[wc]+cityChar[dc]; // no resiliency cost
                cityChar[tc]  = cityChar[tic]+cityChar[fcv]-cityChar[tcvi];
                break;
            case 4:        // (cityChar[dh]>0) && (cityChar[dbh]=0)
                cityChar[dc]  = CalculateDikeCost(cityChar[dh],UnitCostPerVolumeDike,CitySlope,CityWidth,SlopeDike,WidthDikeTop,DikeStartingCostPoint);
                cityChar[vz1] = 0; // there is no protected zone in front of the dike
                cityChar[vz2] = 0; // there is no unprotected zone in front of the dike
                cityChar[vz3] = cityChar[tcvaw]*ProtectedValueRatio*cityChar[dh]/(CEC-cityChar[wh]); // calculate value zone 3
                cityChar[vz4] = cityChar[tcvaw]*(CEC-cityChar[wh]-cityChar[dh])/(CEC-cityChar[wh]); // calculate value zone 4
                cityChar[fcv] = cityChar[vz3]+cityChar[vz4];
                cityChar[tz1] = cityChar[wh];
                cityChar[tz2] = cityChar[wh];
                cityChar[tz3] = cityChar[wh]+cityChar[dh];
                cityChar[tz4] = CEC;
                cityChar[rc]  = 0; // width of the resiliency zone is zero
                cityChar[tic] = cityChar[wc]+cityChar[dc]; // no resiliency cost
                cityChar[tc]  = cityChar[tic]+cityChar[fcv]-cityChar[tcvi];
                break;
            case 5:        // (cityChar[dh]=0) && (cityChar[dbh]>0) && (cityChar[rh]>0) && (cityChar[rh]<cityChar[dbh])
                cityChar[dc]  = CalculateDikeCost(cityChar[dh],UnitCostPerVolumeDike,CitySlope,CityWidth,SlopeDike,WidthDikeTop,DikeStartingCostPoint);
                cityChar[vz1] = cityChar[tcvaw]*DikeUnprotectedValuationRatio*cityChar[rh]/(CEC-cityChar[wh]); // calculate value zone 1
                cityChar[vz2] = cityChar[tcvaw]*DikeUnprotectedValuationRatio*(cityChar[dbh]-cityChar[rh])/(CEC-cityChar[wh]); // calculate value zone 2
                cityChar[vz3] = 0; // dike height is 0
                cityChar[vz4] = cityChar[tcvaw]*(CEC-cityChar[wh]-cityChar[dbh])/(CEC-cityChar[wh]); // calculate value zone 4
                cityChar[fcv] = cityChar[vz1]+cityChar[vz2]+cityChar[vz4]; // , cityChar[dh]=0, so no zone 3
                cityChar[tz1] = cityChar[wh]+cityChar[rh];
                cityChar[tz2] = cityChar[wh]+cityChar[dbh];
                cityChar[tz3] = cityChar[tz2]; // dike height is 0
                cityChar[tz4] = CEC;
                cityChar[rc]  = CalculateResiliencyCost1(cityChar);
                cityChar[tic] = cityChar[wc]+cityChar[dc]+cityChar[rc];
                cityChar[tc]  = cityChar[tic]+cityChar[fcv]-cityChar[tcvi];
                break;
            case 6: // (cityChar[dh]=0) && (cityChar[dbh]>0) && (cityChar[rh]>0) && (cityChar[rh]>=cityChar[dbh])
                cityChar[dc]  = 0;
                cityChar[vz1] = cityChar[tcvaw]*DikeUnprotectedValuationRatio*cityChar[dbh]/(CEC-cityChar[wh]); // calculate value zone 1
                cityChar[vz2] = 0; // calculate value zone 2
                cityChar[vz3] = 0; // cityChar[dh]=0
                cityChar[vz4] = cityChar[tcvaw]*(CEC-cityChar[wh]-cityChar[dbh])/(CEC-cityChar[wh]); // calculate value zone 4
                cityChar[fcv] = cityChar[vz1]+cityChar[vz4];
                cityChar[tz1] = cityChar[wh]+cityChar[dbh];
                cityChar[tz2] = cityChar[tz1];
                cityChar[tz3] = cityChar[tz1];
                cityChar[tz4] = CEC;
                cityChar[rc]  = CalculateResiliencyCost2(cityChar);
                cityChar[tic] = cityChar[wc]+cityChar[dc]+cityChar[rc];
                cityChar[tc]  = cityChar[tic]+cityChar[fcv]-cityChar[tcvi];
                break;
            case 7: // (cityChar[dh]=0) && (cityChar[dbh]>0) && (cityChar[rh]=0)
                cityChar[dc]  = CalculateDikeCost(cityChar[dh],UnitCostPerVolumeDike,CitySlope,CityWidth,SlopeDike,WidthDikeTop,DikeStartingCostPoint);
                cityChar[vz1] = 0; // calculate value zone 1
                cityChar[vz2] = cityChar[tcvaw]*DikeUnprotectedValuationRatio*cityChar[dbh]/(CEC-cityChar[wh]); // calculate value zone 2
                cityChar[vz3] = 0; // calculate value zone 3
                cityChar[vz4] = cityChar[tcvaw]*(CEC-cityChar[wh]-cityChar[dbh])/(CEC-cityChar[wh]); // calculate value zone 4
                cityChar[fcv] = cityChar[vz2]+cityChar[vz4];
                cityChar[tz1] = cityChar[wh];
                cityChar[tz2] = cityChar[wh]+cityChar[dbh];
                cityChar[tz3] = cityChar[tz2];
                cityChar[tz4] = CEC;
                cityChar[rc]  = 0;
                cityChar[tic] = cityChar[wc]+cityChar[dc];
                cityChar[tc]  = cityChar[tic]+cityChar[fcv]-cityChar[tcvi];
                break;
            case 8:  // (cityChar[dh]=0) && (cityChar[dbh]=0) && cityChar[rh]>0
                cityChar[dc]=0;
                cityChar[vz1] = cityChar[tcvaw]*cityChar[rh]/(CEC-cityChar[wh]); // calculate value zone 1
                cityChar[vz2] = 0; // calculate value zone 2
                cityChar[vz3] = 0; // calculate value zone 3
                cityChar[vz4] = cityChar[tcvaw]*(CEC-cityChar[wh]-cityChar[rh])/(CEC-cityChar[wh]); // calculate value zone 4
                cityChar[fcv] = cityChar[vz1]+cityChar[vz4];
                cityChar[tz1] = cityChar[wh]+cityChar[rh];
                cityChar[tz2] = cityChar[tz1];
                cityChar[tz3] = cityChar[tz1];
                cityChar[tz4] = CEC;
                cityChar[rc]  = CalculateResiliencyCost1(cityChar);
                cityChar[tic] = cityChar[wc]+cityChar[rc];
                cityChar[tc]  = cityChar[tic]+cityChar[fcv]-cityChar[tcvi];
                break;
            case 9: // (cityChar[dh]=0) && (cityChar[dbh]=0) && cityChar[rh]=0
                cityChar[fcv] = cityChar[tcvaw];
                cityChar[dc]  = 0;
                cityChar[vz1] = 0; // calculate value zone 1
                cityChar[vz2] = 0; // calculate value zone 2
                cityChar[vz3] = 0; // calculate value zone 3
                cityChar[vz4] = cityChar[tcvaw]; // calculate value zone 4
                cityChar[fcv] = cityChar[vz4];
                cityChar[tz1] = cityChar[wh];
                cityChar[tz2] = cityChar[wh];
                cityChar[tz3] = cityChar[wh];
                cityChar[tz4] = CEC;
                cityChar[rc]  = 0;
                cityChar[tic] = cityChar[wc];
                cityChar[tc]  = cityChar[tcvi]-cityChar[fcv];
                break;
        }

    }
    
   double CalculateDamageResiliantUnprotectedZone1(double sl,double * cityChar)
    //dike base height is higher than resiliency height, there is an unprotected nonResiliant zone
    {
        double washOver=sl-cityChar[wh];
        if (sl<=cityChar[tz1])
        {
            // surge is at or below resilient height
            return(
                   cityChar[vz1]*damageFactor*cityChar[dtr]*
                   washOver*(washOver/2+Basement)/
                   (BH*cityChar[rh]));
        }
        else
        {
            //surge is higher than resilient height
            return(
                   cityChar[vz1]*damageFactor*
                   (cityChar[dtr]*(cityChar[rh]/2+Basement)+ // resilient zone is flooded to the top of the resilient height plus
                    (washOver-cityChar[rh]))/  // resilient zone is flooded above the resilient height
                    BH
                    );
        }
    }
    
    
    
    double CalculateDamageResiliantUnprotectedZone2(double sl,double * cityChar)
    //used when cityChar[rh]>cityChar[dbh], there is no unprotected nonresiliant zone
    {
        double washOver=sl-cityChar[wh];
        if (sl<cityChar[tz1])
        {
            // surge is below dike base height
            return(
                   cityChar[vz1]*damageFactor*
                   cityChar[dtr]*
                   washOver*(washOver/2+Basement)/
                   (BH*cityChar[dbh]));
        }
        else
        {
            //surge is higher than dike base height
            if (washOver<(cityChar[rh]))
                // surge is higher than the dike base, but not exceeding the cityChar[rh]
            {
                return(
                       cityChar[vz1]*damageFactor*
                       cityChar[dtr]*
                       (Basement+washOver-cityChar[dbh]/2)/
                       BH);
                //return(pow(cityChar[vz1]*cityChar[dtr]*cityChar[dbh]*cityChar[dbh]/2+sl-cityChar[tz1]/BH,damageratioexponent));
            }
            else
                // surge is higher than the dike base, and exceeds the cityChar[rh]
            {
                return(
                       cityChar[vz1]*damageFactor*
                       (cityChar[dtr]*
                        (Basement+washOver-cityChar[dbh]/2)+
                        washOver-cityChar[rh])/
                       BH);
            }
        }
    }
    
    
    double CalculateDamageNonResiliantUnprotectedZone(double sl,double * cityChar)
    {
        double washOver=sl-cityChar[tz1];
        if (sl<cityChar[tz2])
        {
            // surge is below dbh
            return(cityChar[vz2]*damageFactor*
                   
                   washOver*(washOver/2+Basement)/
                   (BH*(cityChar[dbh]-cityChar[rh])));
        }
        else
        {
            // surge is higher than dbh
            return(
                   cityChar[vz2]*damageFactor*
                   (Basement+washOver+(cityChar[rh]-cityChar[dbh])/2)/
                   BH);
        }
    }

    double CalculateDamageProtectedZone(double sl,double * cityChar)
    
    {
      double washOver=sl-cityChar[tz2];
       if (sl>=cityChar[tz3]) return(cityChar[vz3]*FailedDikeDamageFactor*damageFactor*
                                     cityChar[dh]*(Basement+cityChar[dh]/2+
                                                      (sl-cityChar[tz3]))/
                                                  (BH*(cityChar[tz3]-cityChar[tz2])));
       else {
         double pf = std::max(pfBase, ((sl-cityChar[tz2])/cityChar[dh]-pfThreshold)/(1-pfThreshold));
         if((double)(rand() % 10000)/10000<(1.0-pf))return(
                                              cityChar[vz3]*intactDikeDamageFactor*damageFactor*
                                              washOver*(Basement+washOver/2)/(BH*(cityChar[tz3]-cityChar[tz2]))); // dike intact
        
        else return(cityChar[vz3]*FailedDikeDamageFactor*damageFactor*
               washOver*(Basement+washOver/2)/(BH*(cityChar[tz3]-cityChar[tz2]))); //dike failed
         }
    }
    
    
    double CalculateDamageAboveDikeProtectionZone(double sl,double * cityChar)
    {
        double washOver=sl-cityChar[tz3];
        return(cityChar[vz4]*damageFactor*
                  washOver*(washOver/2+Basement)/
                  BH/(cityChar[tz4]-cityChar[tz3]));
    }

    


    
#include <iostream>
#include <stdio.h>
#include <math.h>
#include <vector>
#include <fstream>
#include <sstream>
#include <random>
#include <cstring>
    
    //std::random_device rd;
    using namespace std;
    void CalculateDamageVector(double s,double * cityChar,double * damagevector)
    
    {
        memset(damagevector, 0.0, sizeof(double)*8);
        
        int c=(int) cityChar[caseNum];
        double surge=0;
        if (s>Seawall) surge=s*runUpWave-Seawall;
        
        if(surge>cityChar[wh]) //otherwise there will be no damage
        {
            
            switch ( c ) {
                case 0:       // not valid
                {
                    break;
                }
                case 1:       // (cityChar[dh]>0.0) && (cityChar[dbh]>0.0) && (cityChar[rh]>0.0) && (cityChar[rh]<cityChar[dbh])
                {
                    damagevector[dvz1]=CalculateDamageResiliantUnprotectedZone1(surge,cityChar);
                    damagevector[dvFE]=1;
                    if (surge>cityChar[tz1])
                    {
                        damagevector[dvz2]=CalculateDamageNonResiliantUnprotectedZone(surge,cityChar);
                        if (surge>cityChar[tz2])
                        {
                            damagevector[dvz3]=CalculateDamageProtectedZone(surge,cityChar);
                            if (surge>cityChar[tz3]) damagevector[dvz4]=CalculateDamageAboveDikeProtectionZone(surge,cityChar);
                        }
                    }
                    break;
                }
                case 2: // (cityChar[dh]>0.0) && (cityChar[dbh]>0.0) && (cityChar[rh]>0.0) && (cityChar[rh]>=cityChar[dbh])
                {
                    damagevector[dvz1]=CalculateDamageResiliantUnprotectedZone2(surge,cityChar);
                    damagevector[dvFE]=1;
                    // damagevector[dvz2]=0; //there is no nonresilient unprotected zone
                    if (surge>cityChar[tz2])
                    {
                        damagevector[dvz3]=CalculateDamageProtectedZone(surge,cityChar);
                        if (surge>cityChar[tz3]) damagevector[dvz4]=CalculateDamageAboveDikeProtectionZone(surge,cityChar);
                    }
                    break;
                }
                case 3:       // (cityChar[dh]>0.0) && (cityChar[dbh]>0.0) && (cityChar[rh]=0.0)
                {
                    // damagevector[dvz1]=0; //zone 1 does not exist
                    damagevector[dvz2]=CalculateDamageNonResiliantUnprotectedZone(surge,cityChar);
                    damagevector[dvFE]=1.0;
                    if (surge>cityChar[tz2])
                    {
                        damagevector[dvz3]=CalculateDamageProtectedZone(surge,cityChar);
                        if (surge>cityChar[tz3]) damagevector[dvz4]=CalculateDamageAboveDikeProtectionZone(surge,cityChar);
                    }
                    break;
                }
                case 4:       // (cityChar[dh]>0.0) && (cityChar[dbh]=0.0)
                {
                    // damagevector[dvz1]=0;
                    // damagevecotor[2=0;]
                    if (surge>cityChar[tz2])
                    {
                        damagevector[dvz3]=CalculateDamageProtectedZone(surge,cityChar);
                        if (surge>cityChar[tz3]) damagevector[dvz4]=CalculateDamageAboveDikeProtectionZone(surge,cityChar);
                        if (damagevector[dvz3]>0) damagevector[dvFE]=1;
                    }
                    break;
                }
                case 5:       // (cityChar[dh]=0.0) && (cityChar[dbh]>0.0) && (cityChar[rh]>0.0) && (cityChar[rh]<cityChar[dbh])
                {
                    damagevector[dvz1]=CalculateDamageResiliantUnprotectedZone1(surge,cityChar);
                    damagevector[dvFE]=1;
                    if (surge>cityChar[tz1])
                    {
                        damagevector[dvz2]=CalculateDamageNonResiliantUnprotectedZone(surge,cityChar);
                        if (surge>cityChar[tz3])
                        {
                            // damagevector[dvz3]=0;
                            damagevector[dvz4]=CalculateDamageAboveDikeProtectionZone(surge,cityChar);
                        }
                    }
                    break;
                }
                case 6:       // (cityChar[dh]=0.0) && (cityChar[dbh]>0.0) && (cityChar[rh]>0.0) && (cityChar[rh]>=cityChar[dbh])
                {
                    damagevector[dvz1]=CalculateDamageResiliantUnprotectedZone2(surge,cityChar);
                    damagevector[dvFE]=1.0;
                    // damagevector[dvz2]=0;
                    if (surge>cityChar[tz3])
                    {
                        //damagevector[dvz3]=0;
                        damagevector[dvz4]=CalculateDamageAboveDikeProtectionZone(surge,cityChar);
                    }
                    break;
                }
                case 7:       // (cityChar[dh]=0.0) && (cityChar[dbh]>0.0) && (cityChar[rh]=0.0)
                {
                    damagevector[dvz2]=CalculateDamageNonResiliantUnprotectedZone(surge,cityChar);
                    damagevector[dvFE]=1.0;
                    if (surge>cityChar[tz3])
                    {
                        // damagevector[dvz3]=0;
                        damagevector[dvz4]=CalculateDamageAboveDikeProtectionZone(surge,cityChar);
                    }
                    break;
                }
                case 8:       // (cityChar[dh]=0.0) && (cityChar[dbh]=0.0) && (cityChar[rh]>0.0)
                {
                    damagevector[dvFE]=1.0;
                    damagevector[dvz1]=CalculateDamageResiliantUnprotectedZone1(surge,cityChar);
                    // damagevector[dvz2]=0;
                    // damagevector[dvz3]=0
                    if (surge>cityChar[tz1]) damagevector[dvz4]=CalculateDamageAboveDikeProtectionZone(surge,cityChar);
                    break;
                }
                case 9:       // (cityChar[dh]=0.0) && (cityChar[dbh]=0.0) && (cityChar[rh]=0.0)
                {
                    // damagevector[dvz1]=0;
                    // damagevector[dvz2]=0;
                    // damagevector[dvz3]=0;
                    damagevector[dvFE]=1.0;
                    damagevector[dvz4]=CalculateDamageAboveDikeProtectionZone(surge,cityChar);
                    break;
                }
            
            }
            damagevector[dvt]=damagevector[dvz1]+damagevector[dvz2]+damagevector[dvz3]+damagevector[dvz4];
            if (damagevector[dvz3]>0) damagevector[dvBE]=1;
            if(damagevector[dvt]>threshold) {
              damagevector[dvTE]=1.0;
              damagevector[dvt]=damagevector[dvt]+
                                pow(thresholdDamageFraction*(damagevector[dvt]-threshold),thresholdDamageExponent);
            }
          
                
      
    }
    }
      

    
    double evaluateDamageOverTime(double RH,double RP, double WH, double DBH, double DH, int years, 
                                int statesToEvaluate,
                                double* obj_dvt,
                                double* obj_tic,
                                double* obj_r,
                                double* obj_b, 
                                double* obj_dc, 
                                double* obj_rc) 

                                
    /*    void evaluateDamageOverTime(double WH,double RH,double RP, double DBH,double DH,
     double* obj_dvt,
     double* obj_tic,double* obj_netc) */
    
    {
        //        double WH=0;
        //        double RH=0;
        //        double RP=.9;
        //        double DBH=0;
        //        double DH=0;

        int chunks=(int)statesToEvaluate/maxSurgeBlock;
        int innerLoops;
        double surges[maxSurgeBlock*lengthSurgeSequences];
        double surge;
        double staveOffTime=years;
        double damageVector[dvLength]={0,0,0,0,0,0,0,0};
        double damageVectorAccumulated[dvLength]={0,0,0,0,0,0,0,0};
        double perSequenceDamage[statesToEvaluate];
        double city[numCityChar];
        double seqDamage;
        int s=0;
        srand(time(NULL));
        CharacterizeCity (WH,DBH,RH,RP,DH,city);
        std::ifstream SurgeFile;
        SurgeFile.open("surges.bin", ios::in | ios::binary);
        // void CharacterizeCity (double WH,double DBH,double RH,double RP, double dH, double * cityChar) {
        
        for (int w=0;     w<chunks    ; w++){
            SurgeFile.seekg(w*sizeof(surges));//SurgeFile.seekg(0);
            SurgeFile.read((char*)&surges, sizeof(surges));          
            
            if ((w+1)*maxSurgeBlock<statesToEvaluate) innerLoops=maxSurgeBlock;
            else innerLoops=statesToEvaluate-w*maxSurgeBlock;
                for (int state=0; state<innerLoops; state++){
                seqDamage=0;
                for (int y=0; y<years; y++) {
                    memset(damageVector, 0, sizeof(damageVector));
                    surge=surges[state*lengthSurgeSequences+y];
                    if (surge>Seawall){
                        CalculateDamageVector(surge,city, damageVector);
                        damageVectorAccumulated[dvFE]=damageVectorAccumulated[dvFE]+damageVector[dvFE];
                        damageVectorAccumulated[dvt]=damageVectorAccumulated[dvt]+damageVector[dvt];
                        seqDamage=seqDamage+damageVector[dvt];
                        damageVectorAccumulated[dvBE]=damageVectorAccumulated[dvBE]+damageVector[dvBE];
                        damageVectorAccumulated[dvTE]=damageVectorAccumulated[dvTE]+damageVector[dvTE];
                        }
                }
                        

            
                //           if((staveOffTime==years) && (damageVector[dvBE]==1.0)) {staveOffTime=(double)y;};
              }            
        }  
        SurgeFile.close();
        if (damageVectorAccumulated[dvt]==0) damageVectorAccumulated[dvt]=1.0;
        *obj_dvt=damageVectorAccumulated[dvt]/statesToEvaluate;
        *obj_tic=city[tic];
        *obj_r=city[rh];
        *obj_b=city[dbh];
        *obj_dc=city[dc];
        *obj_rc=city[rc];
        return(city[wc]);
    }
    
    
} // extern "C"
