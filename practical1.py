# exercise 1: hashing
import hashlib
import json
m = hashlib.sha256()
m.update(b"Hello COMP!")
# print(m.hexdigest())
data_block = {
    'block_text': 'This is the first block. The Times 14/Jan/19 Rebels hatch bill to delay Brexit.',
    'block_data': [123,234,321,345,645,235,765,234,7456,746,5245,456,568,456,345,457,23],
    'block_meta_data_1': 123,
    'block_meta_data_2': '15/01/2019'
}
json_data = json.dumps(data_block, sort_keys=True)
#print(json_data)
check_sum = hashlib.sha256(json_data.encode('utf-8')).hexdigest()
# print(check_sum)
data_block = json.loads(json_data)

# lecture 6 exercise
# import string
import random
# letters = string.ascii_lowercase
# hashval = "1111111111111111111111111111"
# while hashval[:13]!="000": #(hexadecimal so look for 000 instead of 00000000000 at start)
#     m = hashlib.sha256()
#     nonce = ''.join(random.choice(letters) for i in range(10))
#     choice = ''tacos'
#     value = nonce+choice
#     m.update(b"Hello COMP4137!")
#     hashval = m.hexdigest()

# ":%iAB# X(;Hg*n6x   salad" has 23 0s

# test_pattern=0
# for j in range(target%8):
#     test_pattern+=(1<<(7-j))

target=10
data=" noodles" # last 8 bytes are menu option

prev_hash = "0000137bf291869c7a2de14f1698214649eabdccb8eb743f44b0e00ab0d03806"
#0000701fda1a7bdd73cc103a1211ced3826f51e3077315d97a6766640bf35fbe
#00004513196f080ec21095a7bef59a8d5d87de848d71d05378cc4d1d3991bf82
while True:
    win=True
    #test
    #prev_hash = b'000000046288f4458cdf3f9c579d9a792842cdb505ccbf5c457e42021282f801'
    #text= "TjD^/>Ye^_0<~3&s"
    #data = "  cheese"
    # hash1 = hashlib.sha256(prev_hash+(text+data).encode('utf-8'))
    # print(hash1.hexdigest())
    # break

    #generate 16 random char
    text=''+''.join(chr(random.randint(32,127)) for _ in range(16))
    hash1 = hashlib.sha256(bytearray.fromhex(prev_hash))
    hash1.update((text+data).encode('utf-8'))
    # print(hash1.hexdigest())
    # break
    #check bits entirely 0
    for i in range(target//8):
        if hash1.digest()[i]>0:
            win=False
    if win:
        for j in range(target%8):
            check="{0:08b}".format(hash1.digest()[target//8])
            if int(check[j])>0:
                win=False
    
    # if (hash1.digest()[target//8] & test_pattern):
    #     win=False

    if win:
        print("Match: \""+text+data+"\" with hash "+str(hash1.hexdigest()))
        print("First bytes as bits:")
        for i in range(target//8+1):
            bits1="{0:08b}".format(hash1.digest()[i])
            print(bits1)
        break

# exercise 2: create blockchain
first_block = {
    'block_id': 0,
    'block_data': 'This is the content of the first block',
    'previous_hash': 0
}
json_data = json.dumps(first_block, sort_keys=True)
check_sum = hashlib.sha256(json_data.encode('utf-8')).hexdigest()
first_block['hash'] = check_sum
# print(first_block)
second_block = {
    'block_id': 1,
    'block_data': 'This is the content of the second block',
    'previous_hash': first_block['hash']
}
json_data = json.dumps(second_block, sort_keys=True)
check_sum = hashlib.sha256(json_data.encode('utf-8')).hexdigest()
second_block['hash'] = check_sum
# print(second_block)
third_block = {
    'block_id': 2,
    'block_data': 'This is the content of the third block',
    'previous_hash': second_block['hash']
}
json_data = json.dumps(third_block, sort_keys=True)
check_sum = hashlib.sha256(json_data.encode('utf-8')).hexdigest()
third_block['hash'] = check_sum
# print(third_block)

class Blockchain:
    def __init__(self, blocks):
        self.chain = blocks
    
    # verify hash matches previous_hash for each block
    def verify(self):
        verified = True
        for i in range(len(self.chain)-1):
            if self.chain[i]['block_id'] != 0:
                if self.chain[i+1]['previous_hash'] != self.chain[i]['hash']:
                    print("could not verify blockchain")
                    verified = False
        if verified:
            print("verified")

    def add_block(self):
        new_block = {
            'block_id': self.chain[-1]['block_id'] + 1,
            'block_data': 'This is the content of the newest block',
            'previous_hash': self.chain[-1]['hash']
        }
        json_data = json.dumps(new_block, sort_keys=True)
        check_sum = hashlib.sha256(json_data.encode('utf-8')).hexdigest()
        new_block['hash'] = check_sum
        self.chain.append(new_block)

    # verify given item of data is in data block with given index
    def verify_data(self,index,data):
        if self.chain[index]['block_data'] == data:
            print("data verified")
        else:
            print("data not found")

# initialise blockchain
blockchain = Blockchain([first_block,second_block,third_block])
# print(blockchain.chain)
# blockchain.verify()
for i in range(3):
    blockchain.add_block()
# print(blockchain.chain)
# blockchain.verify_data(0,"This is the content of the first block")

# digital signatures

# generate signing key/verification key pairs
from ecdsa import SigningKey
sk = SigningKey.generate() # uses NIST192p
vk = sk.verifying_key
# sign string
signature = sk.sign(b"message")
# verify signature for message
assert vk.verify(signature, b"message")

# same for serialised data block
sk = SigningKey.generate() # uses NIST192p
vk = sk.verifying_key
data_block = {
    'block_text': 'This is the first block. The Times 14/Jan/19 Rebels hatch bill to delay Brexit.',
    'block_data': [123,234,321,345,645,235,765,234,7456,746,5245,456,568,456,345,457,23],
    'block_meta_data_1': 123,
    'block_meta_data_2': '15/01/2019'
}
json_data = json.dumps(data_block, sort_keys=True)
json_data = json_data.encode('utf-8')
signature = sk.sign(json_data)
# print(vk.verify(signature, json_data))

