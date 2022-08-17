from signer import Signer
import base64
import json

bbs_public_key = 'gh9/xep0FZmatNY1oQgQDDR3TFi6ZgAnXlaRt60Lm4fu0iGJT1+4t69EpHvGG0mqAv1CPIor6G50MzzPzC1sMUGwurGGMnSiUVkFpM6Fs3PnI/QQIsIkb+J6YlMmPBe5'
bbs_secret_key = 'JHwmB38PU07I8d/Zvj/vE1NtjEzjziRTJ4zw09RiHWM='

message= {
    "owner": "Device1-admin",
    "measurements":{
        "temperature":"30oC",
        "humidity":"60%"
    }
}

bbs_signer = Signer(public_key=base64.b64decode(bbs_public_key),secret_key=base64.b64decode(bbs_secret_key))
bbs_signature = bbs_signer.sign_json(json.dumps(message))
f = open("bbs-signed-json.txt", "w")
f.write(base64.b64encode(json.dumps(message).encode()).decode() + "."+ base64.b64encode(bbs_signature).decode())
f.close()
