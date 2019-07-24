
#include <Rcpp.h>
using namespace Rcpp;

// Below is a simple example of exporting a C++ function to R. You can
// source this function into an R session using the Rcpp::sourceCpp 
// function (or via the Source button on the editor toolbar)

// For more on using Rcpp click the Help button on the editor toolbar


#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;
// [[Rcpp::export]]
int surges(){
    ifstream file("surges.csv");
    std::ofstream binWFile;
    binWFile.open("surges.bin", ios::out | ios::binary);
    binWFile.seekp(0);
int sequences = 100000;
int y=200;
    //open "surges.bin" here
    double data[sequences*y];//

    for(int row = 0; row < (sequences-1); ++row)
    {
        std::string line;
        std::getline(file, line);
        if ( !file.good() )
        {std::cout<< "oops, no file! \n";
            break;
        }
        std::stringstream iss(line);   
        for (int col = 0; col < 200; ++col)
        {
            std::string val;
            std::getline(iss, val, ',');
            std::stringstream convertor(val);
            convertor >> data[row*col+col];
        }
        
    }
    binWFile.close();
      cout << data[0] << endl;                 
  cout << data[1] << endl;   
    cout << data[2] << endl;
/*binWFile.write ((char*)&data, sizeof(data));
    if (binWFile.is_open()) cout << "binW open!" <<endl;
        binWFile.close();
    if (file.is_open()) cout << "file open!" <<endl;
    file.close();

  
    double s[10];
            std::ifstream SurgeFile;
    SurgeFile.open("surges.bin", ios::in | ios::binary);
    if (SurgeFile.is_open()) cout << "open!" <<endl;
    SurgeFile.seekg(0);//
    SurgeFile.read((char*)&s, sizeof(s));
    SurgeFile.close();
    cout.precision(5);
    cout << endl <<" first surge:  " << endl;
    cout << fixed<< s[0];
    cout << endl <<" second surge:  " << endl;
    cout << fixed<< s[1];
    cout << endl <<" thrid surge:  "<<  endl;
    cout << fixed<< s[2];
    
       */ 
    return(0);
    

}


/*** R
surges()
 */
