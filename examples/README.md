# Mapping File Specification

In order to map your old pipeline(s) to new pipeline(s), you need to specify the linkage between the "old" and "new" pipeline identifiers.
In the example case, we have 8 pipelines:
```
Untriaged
Product Backlog
Release Backlog
Sprint Backlog
In Progress
Epics In Progress
Ready For Playback
Awaiting Verification
```

Using a pre-destruction backup, you can learn the old pipeline identifiers with a little `jq` run against the "old" board backup:  
`jq -r '.pipelines[] | "\(.name): \(.id)"' zenhub-board.json`  
The output might look a little like this:
```
Untriaged: Old-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA2NDI
Product Backlog: Old-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA1OTU
Release Backlog: Old-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA3MjM
Sprint Backlog: Old-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA1OTY
In Progress: Old-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA1OTc
Epics In Progress: Old-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA3NjA
Ready For Playback: Old-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA3Njg
Awaiting Verification: Old-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA1OTg
```
Then, run that same `jq` over a "new" board backup, after you've re-created your same pipelines as before.
The output should look somewhat similar to what you got before:
```
Untriaged: New-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA2NDI
Product Backlog: New-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA1OTU
Release Backlog: New-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA3MjM
Sprint Backlog: New-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA1OTY
In Progress: New-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA1OTc
Epics In Progress: New-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA3NjA
Ready For Playback: New-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA3Njg
Awaiting Verification: New-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA1OTg
```
Now, you just need to build up a piece of json that does the mapping from old to new for each:
```
[
    {
     "pipeline_name": "Untriaged",
     "old_pipeline_id": "Old-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA2NDI",
     "new_pipeline_id": "New-Oi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA2NDI"
    },
    ...
]
```
The following bit of `jq` gets you 2/3 of the way there, using the old/previous board backup:  
`jq '[.pipelines[] | {pipeline_name:(.name), old_pipeline_id:.id}]' zenhub-board.json`  
You just need to manually add the `"new_pipeline_id"` field for each pipeline element in order to complete the mapping for your old and new boards.
