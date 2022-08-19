from clpkc_rp03 import  CLPKC_RP03
from charm.toolbox.pairinggroup import PairingGroup, ZR
from charm.core.engine.util     import objectToBytes, bytesToObject
from typing import Optional
from ndn.encoding import Name, Component
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo, Component
import asyncio

group = PairingGroup('SS512', secparam=1024)
clpkc = CLPKC_RP03(group)
ID = 'mmlab'
msg = "This is my signed CV"

f = open('master.param', 'r')
bin_data = f.read()
f.close()
params = bytesToObject(bin_data ,group)
f = open(ID + '.key', 'r')
bin_data = f.read()
f.close()
partial_private_key = bytesToObject(bin_data ,group)
secret_value = group.random(ZR)
private_key = clpkc.set_private_key(partial_private_key, secret_value)
public_key = clpkc.set_public_key(params, secret_value)
signature = clpkc.sign(params, private_key, msg)


prefix = "/ndn/gr/edu/mmlab1/aueb/second14"

app = NDNApp()
cert = app.keychain[prefix].default_key().default_cert()

print("Will advertise:" + Name.to_str(cert.name))
@app.route(cert.name)
def cert_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for key")
    app.put_raw_packet(cert.data)


print("Will advertise intermedite key: /ndn/gr/edu/mmlab1/KEY/%F7%9C%E4%D3gL%A2%21")
@app.route("/ndn/gr/edu/mmlab1/KEY/%F7%9C%E4%D3gL%A2%21")
def info_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for intermediate key")
    with open('/home/scn4ndn/mmlab.ndncert', "rb") as f:
        key =  f.read()
        app.put_data(name, content=key, freshness_period=100)

print("Will advertise signed content")
@app.route('/ndn/gr/edu/mmlab1/aueb/second14/cv')
def cv_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for CV")
    raw_data = objectToBytes( signature, group)+ ".".encode() + msg.encode()
    app.put_data(name, content=raw_data, freshness_period=10000)

print("Will advertise DID document")
@app.route('/ndn/gr/edu/mmlab1/aueb/second14/did-doc')
def cv_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for DID document")
    raw_data = objectToBytes( public_key, group)
    app.put_data(name, content=raw_data, freshness_period=10000)


if __name__ == '__main__':
    app.run_forever()