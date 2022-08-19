import json
from canonicalization import JCan
from ursa_bbs_signatures import BlsKeyPair, ProofMessage, ProofMessageType, CreateProofRequest, create_proof
from typing import Optional
from ndn.encoding import Name, Component
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo, Component
import asyncio
import base64


class Prover:
    def _get_proof_messages(self, messages, revealed_messages):
        if not (set(revealed_messages) <= set(messages)):
            raise ValueError("Revealed messages is not subset of the initial messages")
        
        # get messages for the proof
        proof_messages = []
        for msg in messages:
            if msg in revealed_messages:
                proof_messages.append(ProofMessage(msg, ProofMessageType(1)))
            else:
                proof_messages.append(ProofMessage(msg, ProofMessageType(2)))      
        return proof_messages

    def _frame_message(self, message:dict, frame:dict, result:dict={})-> dict:
        if isinstance(message, dict):
            to_iter = message
        elif isinstance(message, list):
            to_iter = range(len(message))
        else: to_iter = message

        for key in to_iter:
            if str(key) in frame:
                if isinstance(message[key], dict):

                    if isinstance(result, list):  result.append({})
                    elif isinstance(result, dict): result[key] = {}
                    else: raise ValueError("Invalid key or value")

                    self._frame_message(message[key], frame[str(key)], result[key])
                elif isinstance(message[key], list):
        
                    if isinstance(result, list):  result.append([])
                    elif isinstance(result, dict): result[key] = []
                    else: raise ValueError("Invalid key or value")
        
                    self._frame_message(message[key], frame[str(key)], result[key])
                else: 
                    result[key] = message[key]

        return result

    def generate_zkp(self, public_key: bytes, message:str, frame:str, signature:bytes) -> list:
        bls_pub_key = BlsKeyPair(public_key=public_key)
        signed_messages = JCan(json.loads(message))
        revealed_message_json = self._frame_message(json.loads(message),json.loads(frame))
        revealed_messages = JCan(revealed_message_json)

        # get the proof messages
        proof_messages = self._get_proof_messages(signed_messages, revealed_messages)

        # get bbs key from bls key (the bls key + the generators)
        claims = len(signed_messages)
        bbs_pub_key = bls_pub_key.get_bbs_key(claims)

        # create proof
        proof_request = CreateProofRequest(public_key=bbs_pub_key,
                                    messages=proof_messages, 
                                    signature=signature, 
                                    nonce=b'PROOF_NONCE') #<---------Fix that

        proof = create_proof(proof_request)
        return claims, json.dumps(revealed_message_json), proof

prefix = "/ndn/gr/edu/mmlab1/aueb/second14"
bbs_public_key = 'gh9/xep0FZmatNY1oQgQDDR3TFi6ZgAnXlaRt60Lm4fu0iGJT1+4t69EpHvGG0mqAv1CPIor6G50MzzPzC1sMUGwurGGMnSiUVkFpM6Fs3PnI/QQIsIkb+J6YlMmPBe5'
    
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
@app.route('/ndn/gr/edu/mmlab1/aueb/second14/measurement')
def cv_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for measurement")
    frame ={
        "measurements":{
            "temperature":"",
        }
    }
    f = open("bbs-signed-json.txt", "r")
    signed_json = f.read()
    f.close()
    b64message = signed_json.split(".")[0]
    b64bbs_signature = signed_json.split(".")[1]
    message= json.loads(base64.b64decode(b64message))
    bbs_signature = base64.b64decode(b64bbs_signature)
    bbs_prover = Prover()
    claims, revealed_message, zkp = bbs_prover.generate_zkp(public_key=base64.b64decode(bbs_public_key), message=json.dumps(message), frame=json.dumps(frame), signature=bbs_signature)
    raw_data = base64.b64encode(json.dumps(revealed_message).encode()).decode() + "."+ base64.b64encode(zkp).decode()+ "." + str(claims)
    app.put_data(name, content=str.encode(raw_data), freshness_period=10000)

if __name__ == '__main__':
    app.run_forever()

