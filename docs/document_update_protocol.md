# Update protocol

We need to be able to send messages to the server, telling it we have modified this portion of text, and so one. We need a clear protocol defined for that.

We will base our protocol on a "micro-commits" system. All modification will be recorded, sent to the server, and played back.

It happens by chance that [ace](http://ace.c9.io) has such a event system, with hookable function, directly built into ace. We will use that.

## event messages

they all have the following structure:

```json

{
    "type": "change",
    "data": {
        "action": "insertText",
        "range": {
            "start": {
                "row": 0,
                "column": 0
            },
            "end": {
                "row": 0,
                "column": 1
            }
        }
        "text": "#"
    }
}
```

action | what changes
--- | ---
`insertText` | We have a data.text attribute. The range will always have the same row. if multiple lines have been altered, multiple events are sent.
`insertLines` | We have an array data.lines containing the inserted lines. 
`removeText` | same as `insertText`, but to remove
`removeLines` | same as `insertLines`, but to remove

## Server response

with each commit, the server will answer with the fully rendered document, the commits recieved since last time the client contacted the server, if any.

This gives us the following json response:

```json
{
    "events": [{"listofevents": "..."}],
    "render": "<h1>blblblbl</h1>"
}
```

## Inner event storage

We need to store events for as long as we haven't sent them to all the clients. At least as long as the server is alive.

I propose to include to the `app` object two new properties: `app.deltas` and `app.client_states`. Their structure will be as follows.

### `app.deltas`

```json
{
    "documentid1": [
        {"event": 1},
        {"event": 2},
        ...
    ],
    "documentid2": [
        {"event": 1},
        ...
    ]
}
```

### `app.client_states

```json
{
    "client_id1_stored_in_session_dict": {
        "document_id1": "int representing the last accessed app.deltas['document_id']",
        "document_id2": "..."
    },
    "client_id2_stored_in_session_dict": "..."
}
```
