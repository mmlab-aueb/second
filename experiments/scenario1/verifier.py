import json
from canonicalization import JCan
from ursa_bbs_signatures import BlsKeyPair, VerifyProofRequest, verify_proof

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


if __name__ == '__main__':
    import base64
    import json
    bbs_public_key = 'gh9/xep0FZmatNY1oQgQDDR3TFi6ZgAnXlaRt60Lm4fu0iGJT1+4t69EpHvGG0mqAv1CPIor6G50MzzPzC1sMUGwurGGMnSiUVkFpM6Fs3PnI/QQIsIkb+J6YlMmPBe5'
    f = open("bbs-signed-private.txt", "r")
    signed_json = f.read()
    f.close()
    bbs_verifier = Verifier()
    b64revealed_message = signed_json.split(".")[0]
    b64zkp = signed_json.split(".")[1]
    claims = int(signed_json.split(".")[2])
    revealed_message= json.loads(base64.b64decode(b64revealed_message))
    zkp = base64.b64decode(b64zkp)
    verification = bbs_verifier.verify_zkp(public_key=base64.b64decode(bbs_public_key), message=revealed_message, claims=claims, zkp=zkp )
    print(verification)