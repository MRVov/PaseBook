

import hmac, base64, struct, hashlib, time

def get_token(secret, digest_mode=hashlib.sha1, intervals_no=None):
    if intervals_no == None:
        intervals_no = int(time.time()) // 30
    key = base64.b32decode(secret)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, digest_mode).digest()
    o = ord(h[19]) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h
   
print get_token('xxx')