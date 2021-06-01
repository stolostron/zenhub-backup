# SOMEONE DELETED YOUR ZENHUB BOARD!

It's true - everyone in your org has the ability to delete your entire Zenhub board.
That can be painful, especially if you have a lot of work that went into issue prioritization, pipeline grooming, and so on.

What do you do?  Hopefully you backed that sucka up!  How, you ask?  Well, this is how!

# Actions

 - Backup
 - Restore

# Required Environment Variables

## Needed for Authentication
```
ZENHUB_API_TOKEN
```
Learn about yours here: https://github.com/ZenHubIO/API#authentication

## Needed for Board Identification
```
ZENHUB_WORKSPACE_ID
GITHUB_REPO_ID
```

You can learn your `ZENHUB_WORKSPACE_ID` and `GITHUB_REPO_ID` by inspecting your Zenhub board URL - it will look something like this:
```
https://app.zenhub.com/workspaces/board_name-{ZENHUB_WORKSPACE_ID}/board?repos={GITHUB_REPO_ID}
```

## Needed for File Identification
```
ZENHUB_BOARD_JSON_FILE=zenhub-board.json
PIPELINE_MAPPING_JSON_FILE=pipeline-map.json
```

These file locations are customizable and completely up to you.

# Operations

Before the big day comes when your Zenhub board vaporizes, grab a copy of the current state.  Maybe back up on a cron.

## Running a Backup

The Python code lives in this repo under `python/`.  Grab the Python prereqs:  
`pip3 install -r requirements.txt`

Now, set up your environment variables and give the backup a try:
```
export ZENHUB_API_TOKEN=<my secret API token, shhhh>
export GITHUB_REPO_ID=<my github repo>
export ZENHUB_WORKSPACE_ID=<my zenhub workspace>
export ZENHUB_BOARD_JSON_FILE=zenhub-board.json
python3 zenhub-backup.py
```

With any luck, you'll get your `zenhub-board.json` file as specified:
```
Retrieving Zenhub board...
Writing "zenhub-board.json"...
Backup complete.
```

This json file neatly encapsulates your entire Zenhub board in its current state.

## Running a Restore

The one additional thing that you'll need for a restore action is a mapping file that maps pipeline identifiers from "old" to "new" (in case they have changed).
There is an example json named `examples/pipeline-map.json` in this repo that shows how it's structured.  It's just an array of elements that map the pipeline identifiers (and names, for readability).  You can learn your own pipeline names and IDs with this bit of `jq` from an existing backup you've made:

```
jq '[.pipelines[] | {pipeline_name:.name, old_pipeline_id:.id}]' zenhub-board.json
```
If you've recreated your pipelines, another backup (to a new name!) will give you the key to your new pipeline IDs to insert into your `pipeline-map.json`.

You can get a nice summary of how many issues are in each pipeline with this `jq`:
```
jq -r '.pipelines[] | "\(.name): \(.issues | length)"' zenhub-board.json
```

As before, set your environment variables - and try a dry run first:
```
export ZENHUB_API_TOKEN=<my secret API token, shhhh>
export GITHUB_REPO_ID=<my github repo>
export ZENHUB_WORKSPACE_ID=<my zenhub workspace>
export ZENHUB_BOARD_JSON_FILE=zenhub-board.json
export PIPELINE_MAPPING_JSON_FILE=pipeline-map.json
export ZENHUB_BOARD_DRY_RUN=True
python3 zenhub-restore.py 
```

You will see copious output similar to the following:
```
Begin processing...
ZENHUB_BOARD_DRY_RUN is not set to 'False', so dry run it is...
Untriaged: Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA2NDI -> Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA2NDI
https://api.zenhub.com/p2/workspaces/{ZENHUB_WORKSPACE_ID}/repositories/{GITHUB_REPO_ID}/issues/12724/moves
{'pipeline_id': 'Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA2NDI', 'position': 'bottom'}
...
Done.
```
When that is successful (and doesn't complain about missing pipelines, for example) you're ready for the big leagues:
```
export ZENHUB_BOARD_DRY_RUN=False
python3 zenhub-restore.py
```
If luck is once more on your side, you will see copious output similar to the following:
```
Begin processing...
ZENHUB_BOARD_DRY_RUN is set to 'False' so this is for real...
Untriaged: Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA2NDI -> Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzIzNTA2NDI
<Response [200]>
...
Done.
```

