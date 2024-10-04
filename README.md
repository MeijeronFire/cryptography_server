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

## Cryptographic scheme

Lorem Ipsum dolor...

## Protocol info

Sit amet consecitur...

## Build info
