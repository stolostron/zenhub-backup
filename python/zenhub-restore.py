#!/usr/bin/env python

from zenhub import Zenhub # the move issue API failed; fellback on requests library
import json
import requests
import os

# Update these variables with the project settings
ZENHUB_BOARD_DRY_RUN = 'True' if os.getenv('ZENHUB_BOARD_DRY_RUN') is None else os.getenv('ZENHUB_BOARD_DRY_RUN')
ZENHUB_API = 'https://api.zenhub.com'
ZENHUB_API_TOKEN = os.getenv('ZENHUB_API_TOKEN')
GITHUB_REPO_ID = os.getenv('GITHUB_REPO_ID')
ZENHUB_WORKSPACE_ID = os.getenv('ZENHUB_WORKSPACE_ID')
AUTH_HEADER = {'X-Authentication-Token': '%s' % ZENHUB_API_TOKEN}
ZENHUB_BOARD_JSON_FILE = 'zenhub-board.json' if os.getenv('ZENHUB_BOARD_JSON_FILE') is None else os.getenv('ZENHUB_BOARD_JSON_FILE')
PIPELINE_MAPPING_JSON_FILE = 'pipeline-map.json' if os.getenv('PIPELINE_MAPPING_JSON_FILE') is None else os.getenv('PIPELINE_MAPPING_JSON_FILE')

if ZENHUB_API_TOKEN is None or GITHUB_REPO_ID is None or ZENHUB_WORKSPACE_ID is None:
    print("ERROR: One or more of the required environment variables were not found: ZENHUB_API_TOKEN, GITHUB_REPO_ID, ZENHUB_WORKSPACE_ID")
    exit(1)

# Details on how to find each of the required parameters
# https://github.com/ZenHubIO/API#move-an-issue-between-pipelines
ISSUES_API = '%s/p2/workspaces/%s/repositories/%s/issues' % (ZENHUB_API, ZENHUB_WORKSPACE_ID, GITHUB_REPO_ID)

def restore_board(ZENHUB_BOARD_JSON_FILE, PIPELINE_MAPPING_JSON_FILE):
    f = open(ZENHUB_BOARD_JSON_FILE, 'r')
    board = json.loads(f.read())
    f.close
    f = open(PIPELINE_MAPPING_JSON_FILE, 'r')
    pipeline_map = json.loads(f.read())
    f.close
    for pipeline in board['pipelines']:
        # Find the mapping from old pipeline to new pipeline
        new_pipeline = 'undefined'
        for pipe_map in pipeline_map:
            if pipe_map['old_pipeline_id'] == pipeline['id']:
                new_pipeline = pipe_map['new_pipeline_id']
        if new_pipeline == 'undefined':
            print('Unable to find a mapping for old pipeline %s/%s to a new pipeline' % (pipeline['name'], pipeline['id']))
            exit(1)
        print('%s: %s -> %s' % (pipeline['name'], pipeline['id'], new_pipeline))
        issues_list = pipeline['issues']
        for issue in issues_list:
            move_issue(issue['issue_number'], new_pipeline)

def move_issue(issue_id, pipeline_id):
    pipeline_params = {
        'pipeline_id': pipeline_id,
        'position': 'bottom'
    }
    rate_pause = 0
    move_url = '%s/%s/moves' % (ISSUES_API, issue_id)
    if ZENHUB_BOARD_DRY_RUN == 'False':
        response = requests.post(move_url, headers=AUTH_HEADER, data=pipeline_params)
        print(response)
        if response.status_code != 200:
            print('ERROR: Could not move %s' % issue)
            print(response.text)
            exit(1)
        rate_pause = rate_pause + 1
        if(rate_pause % 20) == 0:
            print('Pause for API Rate Limit: 10s')
            time.sleep(10)
    else:
        print(move_url)
        print(pipeline_params)

def main():
    print('\nBegin processing...')
    if ZENHUB_BOARD_DRY_RUN == 'False':
        print('ZENHUB_BOARD_DRY_RUN is set to \'False\' so this is for real...')
    else:
        print('ZENHUB_BOARD_DRY_RUN is not set to \'False\', so dry run it is...')

    restore_board(ZENHUB_BOARD_JSON_FILE, PIPELINE_MAPPING_JSON_FILE)

    print('\nDone.')

main()
