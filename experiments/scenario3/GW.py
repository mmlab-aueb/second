from typing import Optional
from ndn.encoding import Name, Component
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo, Component

import os
import json
import asyncio

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


async def satisfy_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    interest_name = "/node10/cv"
    print("Communicating with producer...")
    data_name, meta_info, content =  await express_interest(interest_name)
    raw_data = bytes(content)
    app.put_data(name, content=raw_data, freshness_period=10000) 

async def express_interest(insterest_name):
    try:
        loop = asyncio.new_event_loop()
        data_name, meta_info, content = await app.express_interest(
            insterest_name,
            must_be_fresh=True,
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
    interest_name = "/node10"
    print("Searching for producer...")
    data_name, meta_info, content = await express_interest(interest_name)
    raw_data = bytes(content)
    print(raw_data)
    print("Will advertise /ndn/gr/edu/mmlab1/aueb/second14/cv")	
    @app.route('/ndn/gr/edu/mmlab1/aueb/second14/cv')
    def data_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
        print("Received interest in nested function")
        asyncio.ensure_future(satisfy_interest(name, param, _app_param))

   

if __name__ == '__main__':
    app.run_forever(after_start=run())
