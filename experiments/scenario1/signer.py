import json
from canonicalization import JCan
from ursa_bbs_signatures import BlsKeyPair, SignRequest, sign

class Signer:
    def __init__(self, public_key: bytes, secret_key: bytes) -> None:
        self.bls_key_pair = BlsKeyPair(public_key=public_key, secret_key=secret_key) 

    def sign_json(self, message: str) -> bytes:
        messages_to_sign = JCan(json.loads(message))
        # create signature
        sign_request = SignRequest(key_pair=self.bls_key_pair, messages=messages_to_sign)
        signature = sign(sign_request)
        return signature