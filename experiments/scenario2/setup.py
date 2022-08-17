from clpkc_rp03 import  CLPKC_RP03
from charm.toolbox.pairinggroup import PairingGroup
from charm.core.engine.util     import objectToBytes

group = PairingGroup('SS512', secparam=1024)
clpkc = CLPKC_RP03(group)
(params, master_key) = clpkc.setup()
ID = 'mmlab'
partial_private_key = clpkc.partial_private_key_extract(master_key, ID)

f = open('master.param', 'wb')
f.write( objectToBytes( params, group))
f.close()

f = open(ID + '.key', 'wb')
f.write( objectToBytes( partial_private_key, group))
f.close()

