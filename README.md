# Cryptography Server

This repo is to host the code neccesary for running the cryptography server and client. More information on the protocol and cryptographic scheme will follow.
Globally it works like so:

client 1 -> server -> any client -> interpretation and decryption

## Server

The server is quite simple. It is a flask server running two routes:
1. Data retrieval: `/send`
2. Data posing `/receive`

### Data posting
Whenever `/send` receives a POST request, it transcribes it into a dict and adds it to an array:
```python
if requests.method == "POST":
    data = requests.form.to_dict()
    ALL_MSGS.append(data) 
```
### data receiving
To limit the amount of data being transmitted, we had to think of a solution to send only the required amount. This is done by adding an argument with the get request. This argument describes the index of the most recently accessed element: i.e. the client compares a local version of `ALL_MSGS`, tells the server how many elements it _has_ and the server responds with elements the client _doesn't_ have, by sending all entries after the provided index:
```python
@app.route("/receive", methods=["GET"])
def receive():
    args = requests.args
    requested_index = args.get("current", default=0, type=int) # 0 indexed
    return ALL_MSGS[requested_index:len(ALL_MSGS)] # return all messages from the requested to the latest.
```

## client
The client is quite simple and it works pretty much as expected with the server. Its sends data and only requests onseen messages. All interesting information is in the cryptographic scheme, but still, it is good to know that it sends four pieces of data:
```python
    parameters = {
            "time": floor(timestamp),
            "hash": msg_hash,
            "msg": message_plain,
            "userID": userID
    }
```
But all of it is pretty self-explanatory. The time is the unix timestamp
when it has been sent, the hash is the hash (algorithm tbd) of msg and the usrID is a unique number defining who sent it.

## Cryptographic scheme
Neccesary algorithms:
- prime number generator -> write about how the faster mod\_exp worked.
- random number generator
- RSA encryption
- Hashing algorithm (sha256?)

The cryptographic scheme is pretty simple. The message is encrypted first with the private key of the sender, after which it is hashed, after which it is encrypted again with the public key of the receiver, after which this doubly-encrypted message is sent in msg, and the hash after the first encryption is added.

When a client reads the database he cannot read anything, since it is encrypted. He can decode it with his private key first to. If the hash of whatever he gets is the same as the hash that was sent, it must be meant for him, since a different key would yield a different message and therefore a different hash. Anyway, once he makes sure that the message is meant for him, he can consult the provided user ID and decrypt it with the public key of the user. This ensures that it was actually sent by the user, since any other one won't be decrypted with their public key.

To summarize: an observer does not know to whom any message was sent and what was sent. The only available information is _who_ sent a message.

More info: for RSA, the keysize is _2048 bits_. For some reason (check), this allows a size of (2048/8) - 42 bytes as a max size. The max size that we want is 256 bits, so that means that we do not need to take any steps to ensure that the message is divided into blocks.

## Build info
