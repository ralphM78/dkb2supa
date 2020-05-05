# dkb2supa

This script converts CSV account reports from [Deutsche Kreditbank (DKB)](https://www.dkb.de) to
[SUPA CSV](https://subsembly.com/supa.html) for [Banking4](https://subsembly.com/banking4.html)
 

## Requirements

To run this script you need Python 3 and [schwifty](https://pypi.org/project/schwifty/) .

```
pip install schwifty
```


## How to run this script

```
./dkb2supa.py -h
usage: dkb2supa.py [-h] -i INPUTFILE -o OUTPUTFILE [--iban DE820000000000]
                   [--cur EUR]

Convert DKB CSV into SUPA CSV.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --input INPUTFILE
                        DKB CSV input file
  -o OUTPUTFILE, --output OUTPUTFILE
                        SUPA formated CSV output file
  --iban DE820000000000
                        Optionally your IBAN
  --cur EUR             Optional Currency. Default is EUR
```

