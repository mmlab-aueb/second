from ndn.encoding import Name, Component
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure

import os
import json
import asyncio


app = NDNApp()

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
    interest_name = "/ndn/gr/edu/mmlab1/aueb/second14/cv"
    data_name, meta_info, content = await express_interest(interest_name)
    raw_data = bytes(content)
    print(raw_data)	
    app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=run())
