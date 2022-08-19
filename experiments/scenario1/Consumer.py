import json
from canonicalization import JCan
from ursa_bbs_signatures import BlsKeyPair, VerifyProofRequest, verify_proof
from ndn.encoding import Name, Component
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
import base64
import time
import asyncio

class Verifier:
    def verify_zkp(self,public_key: bytes, message:str, claims:int, zkp:bytes) -> bool:
        bls_pub_key = BlsKeyPair(public_key=public_key)
        revealed_messages = JCan(json.loads(message))
        bbs_pub_key = bls_pub_key.get_bbs_key(claims)
        proof_verify_request = VerifyProofRequest(public_key=bbs_pub_key,
                                          proof=zkp,
                                          messages=revealed_messages,
                                          nonce=b'PROOF_NONCE')#<---fix that
    
        proof_verify_res = verify_proof(proof_verify_request)
        return proof_verify_res


app = NDNApp()
bbs_public_key = 'gh9/xep0FZmatNY1oQgQDDR3TFi6ZgAnXlaRt60Lm4fu0iGJT1+4t69EpHvGG0mqAv1CPIor6G50MzzPzC1sMUGwurGGMnSiUVkFpM6Fs3PnI/QQIsIkb+J6YlMmPBe5'

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
    interest_name = "/ndn/gr/edu/mmlab1/aueb/second14/measurement"
    print ('Sending interest for signed content')
    start_time = time.time()
    data_name, meta_info, content = await express_interest(interest_name)
    print (f'{time.time() - start_time} \t received item') 	
    raw_data = bytes(content).decode()
    signed_json = raw_data
    bbs_verifier = Verifier()
    b64revealed_message = signed_json.split(".")[0]
    b64zkp = signed_json.split(".")[1]
    claims = int(signed_json.split(".")[2])
    revealed_message= json.loads(base64.b64decode(b64revealed_message))
    zkp = base64.b64decode(b64zkp)
    verification = bbs_verifier.verify_zkp(public_key=base64.b64decode(bbs_public_key), message=revealed_message, claims=claims, zkp=zkp )
    print(revealed_message)
    print(verification)
    app.shutdown() 

if __name__ == '__main__':
    app.run_forever(after_start=run())