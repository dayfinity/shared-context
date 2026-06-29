# Collaborative contract system with memory and export flow
import hashlib
import json
import uuid
import time

class Memory:
    def __init__(self):
        self.data = {}

    def put(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

class FileSystem:
    def __init__(self):
        self.files = {}

    def write(self, name, content):
        self.files[name] = content

    def read(self, name):
        return self.files.get(name)

def create_contract(user, project, task):
    return {
        "id": str(uuid.uuid4()),
        "user": user,
        "project": project,
        "task": task,
        "timestamp": time.time()
    }

def encode(contract):
    return json.dumps(contract, sort_keys=True)

def hash_contract(encoded):
    return hashlib.sha256(encoded.encode()).hexdigest()

def sign(hash_value, secret):
    return hashlib.sha256(f"{hash_value}:{secret}".encode()).hexdigest()

def verify(hash_value, sig, secret):
    return sign(hash_value, secret) == sig

def workflow():
    memory = Memory()
    fs = FileSystem()

    contract = create_contract("Alice", "ProjectX", "Design Review")
    encoded = encode(contract)
    h = hash_contract(encoded)

    memory.put(h, contract)
    fs.write("contract.json", encoded)

    sig = sign(h, "workspace_key")
    valid = verify(h, sig, "workspace_key")

    print("Hash:", h)
    print("Signature:", sig)
    print("Valid:", valid)
