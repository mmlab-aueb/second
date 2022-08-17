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
f = open('signature.txt', 'r')
bin_data = f.read()
f.close()
public_key = bytesToObject(bin_data.split(".")[0] ,group)
signature = bytesToObject(bin_data.split(".")[1] ,group)
verification = clpkc.verify(params, msg, signature, ID,  public_key)
print(verification)