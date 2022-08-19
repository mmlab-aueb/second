# SECOND Experiment scenarios
## About
These are SECOND experiment scenarios and their corresponding scripts

## Scenario 1: Private content retrieval using ZKP
### Description
In this scenario a `Producer` acts as a storage node that hosts a JSON-encoded
item, singed using the BBS+ digital signature algorithm. This item represents
the measurements of an IoT device. A `Consumer` sends an interest for a subset of these measurements
by providing a "frame". The Producer generates the requested subset, calculates
a ZKP that proves its correctness, and sends a data packet that includes the signed
object. Finally, the Consumer validates the provided ZKP

### Preparation
This scenario depends on python wrapper of ursa-bbs-signatures library. Install it using

```
python3 -m pip install ursa-bbs-signatures
```

### Execution

Initially run the `setup.py` script that will generate the singed object. The signed
object must be placed in the same node as the `Producer.py` script. Then, run
the `Producer.py` script. Finally, run the `Consumer.py` script.

Expected output: the `Consumer.py` script should display the requested subset of
measurements and output the ZKP verification result.

## Scenario 2: Human readable DIDs
### Description
In this scenario a Producer uses certificateless public key cryptography to generate
human readable DIDs, used for protecting content items. The DID document that corresponds
to the Producer's DID is not included in the content item, instead it is retrieved
using legacy NDN operations. This scenario demonstrates that due to the caching
properties of NDN, DID documents are retrieved fast. The scenario includes two
Consumers, which both request the same item and then request the DID document
required for validating the retrieved item. It is shown that the second Consumer
retrieves the DID document much faster. 

### Preparation
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
make
sudo make install
sudo ldconfig
```

Then install charm crypto as follows:

```
git clone https://github.com/JHUISI/charm.git
cd charm
./configure.sh
make
sudo make install
```
### Execution
Initially run the `setup.py` script that will generate the system parameters and the
pre-master secret key of the Producer. The file that contains the system parameters
must be placed in all nodes. The pre-master secret key
object must be placed in the same node as the `Producer.py` script. Then, run
the `Producer.py` script. Finally, run the `Consumer1.py` script and then the
`Consumer2.py`.

Expected output: the `Consumer1.py` script should display the requested item and the
signature verification result. Similarly, `Consumer2.py`should display the same information
but it should be executed must faster, since it will used a cached copy of the DID
document.

## Scenario 3: Authorized prefix advertisements
In this scenario a node acts as a `Gateway` to the NDN testbed. All Producers interact
with the NDN testbed through this Gateway. Producers send `advertisements` to the
Gateway, as well as Verifiable Credential that proves that they are authorized to
advertise the specific prefix. If the Verifiable Credential is valid, the Gateway
forwards the advertisement to the NDN testbed. An interest for an item advertised
this way will flow to the Producer through the Gateway. 

### Description
### Preparation
This scenario does not depend on any external package.

### Execution
Run the `Producer.py` script. Then, run the `GW.py` script. Finally, run the `Consumer.py` script.

Expected output: the `Consumer.py` script should display the requested item.
Similarly, the `GW.py` and the `Producer.py` script should display output that
will show that the interest message went to the Producer through the GW.