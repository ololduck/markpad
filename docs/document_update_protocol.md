# Update protocol

We need to be able to send messages to the server, telling it we have modified this portion of text, and so one. We need a clear protocol defined for that.

We will base our protocol on a "micro-commits" system. All modification will be recorded, sent to the server, and played back.

## Events triggering a update message

event | reason
--- | ---
X ms elapsed since last update | we need to update periodically, even if nothing needs to be updated. We do so to keep being notified of text changes by the server.
Pasted something | if the user has pasted a content, we need to send it right away
Deleted something | we need to get the selection deleted and notify the server this selected portion of text does not exist anymore.

## What will be the message layout?

JSON. Json is easily parsed in JS, and the python `json` module is quite good. So JSON it will be. (or maybe messagepack, since may have to send lots of data?)

the proposed structure is the following: 

```json
{
    "events": [
        {
            "type": "'i' for insertion, 'd' for deletion",
            "data": {
                "position": int,
                "text": "Here the added or removed string"
            }
        },
        ...
    ]
}
```

Please note the `"events"` key, wich is an array. If communication with the server is not possible, the message shall be saved.

## Now, the server response

To each update event, the server will respond with the micro-commits recieved since last update, along with a complete render of the file(?). This means we must be able to identify the connected client. And to detect his absence.

```json

{
    "events": [
        {
            ... # standard event
        }
    ],
    "render": "here the full document render"
}
```

