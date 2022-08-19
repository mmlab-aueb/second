from clpkc_rp03 import  CLPKC_RP03
from charm.toolbox.pairinggroup import PairingGroup, ZR
from charm.core.engine.util     import objectToBytes, bytesToObject
from ndn.encoding import Name, Component
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure

group = PairingGroup('SS512', secparam=1024)
clpkc = CLPKC_RP03(group)
ID = 'mmlab'

f = open('master.param', 'r')
bin_data = f.read()
f.close()
params = bytesToObject(bin_data ,group)



import time
import asyncio

app = NDNApp()


async def express_interest(insterest_name, must_be_fresh=False):
    try:
        loop = asyncio.new_event_loop()
        data_name, meta_info, content = await app.express_interest(
            insterest_name,
            must_be_fresh=must_be_fresh,
            can_be_prefix=True,
            lifetime=6000)
        return  data_name, meta_info, content
    except InterestNack as e:
        # A NACK is received
        print(f'Nacked with reason={e.reason}')
    except InterestTimeout:
        # Interest times out
        print(f'Timeout')
    except InterestCanceled:
        # Connection to NFD is broken
        print(f'Canceled')
    except ValidationFailure:
        # Validation failure
        print(f'Data failed to validate')

async def run():
    
    interest_name = "/ndn/gr/edu/mmlab1/aueb/second14/cv"
    print ('Sending interest for signed content')
    start_time = time.time()
    data_name, meta_info, content = await express_interest(interest_name, True)
    print (f'{time.time() - start_time} \t received item') 	
    raw_data = bytes(content).decode()
    print(raw_data)
    signature = bytesToObject(raw_data.split(".")[0] ,group)
    msg = raw_data.split(".")[1] 
    interest_name = "/ndn/gr/edu/mmlab1/aueb/second14/did-doc"
    print ('Sending interest for DID document')
    start_time = time.time()
    data_name, meta_info, content = await express_interest(interest_name)
    print (f'{time.time() - start_time} \t received item') 	
    raw_data = bytes(content).decode()
    print(raw_data)
    public_key = bytesToObject(raw_data ,group)
    verification = clpkc.verify(params, msg, signature, ID,  public_key)
    print(verification) 
    app.shutdown() 

if __name__ == '__main__':
    app.run_forever(after_start=run())