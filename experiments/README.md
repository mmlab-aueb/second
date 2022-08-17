# SECOND Experiment scenarios
## About
These are SECOND experiment scenarios and their corresponding scripts

## Scenario 1: Private content retrieval using ZKP
### Description
### Execution
This scenario depends on python wrapper of ursa-bbs-signatures library. Install it using

```
python3 -m pip install ursa-bbs-signatures
```

## Scenario 2: Human readable DIDs
### Execution
This scenario depends on [charm crypto](https://github.com/JHUISI/charm). Install
it dependencies using the following commands.

Install [gmp](https://gmplib.org/)

```
sudo apt install libgmp-dev
```

Install [pbc](https://crypto.stanford.edu/pbc/download.html)

```
sudo apt-get install bison
sudo apt-get install flex
wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz
tar -xzvf pbc-0.5.14.tar.gz
cd pbc-0.5.14.tar.gz
./configure LDFLAGS="-lgmp"
./make
sudo ./make install
sudo ldconfig
```

Then install charm crypto as follows:

```
git clone https://github.com/JHUISI/charm.git
cd charm
./configure.sh
./make
sudo ./make install
```
