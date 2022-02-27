# Topsis

# Installation
To install the package use
```
pip install Topsis-101917193-Vidushi==0.1
```
Usage
```
from Topsis-101917193-Vidushi import topsis

#creating the topsis object
#t = topsis(INPUT_FILENAME,WEIGHT_STRING,IMPACT_STRING,OUTPUT_FILENAME)

# Example
t = tp.topsis("101917193.csv", "1,1,1,2,1", "+,-,-,+,-", "output.csv")

#Calculate TOPSIS
t.calculate()
```
