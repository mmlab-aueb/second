from clpkc_rp03 import  CLPKC_RP03
from charm.toolbox.pairinggroup import PairingGroup, ZR
from charm.core.engine.util     import objectToBytes, bytesToObject


group = PairingGroup('SS512', secparam=1024)
clpkc = CLPKC_RP03(group)
ID = 'mmlab'
msg = "This is a message to sign"

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
f = open("signature.txt", "wb")
f.write(objectToBytes( public_key, group) + ".".encode() + objectToBytes( signature, group))
f.close()
