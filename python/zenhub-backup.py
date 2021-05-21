#!/usr/bin/env python

from zenhub import Zenhub # the move issue API failed; fellback on requests library
import json
import os

# Update these variables with the project settings
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

def print_board():
    zh = Zenhub(ZENHUB_API_TOKEN)
    print('\nRetrieving Zenhub board...')

    board = zh.get_repository_board(ZENHUB_WORKSPACE_ID, GITHUB_REPO_ID)
    print('Writing "%s"...' % ZENHUB_BOARD_JSON_FILE)
    f = open(ZENHUB_BOARD_JSON_FILE, 'w')
    f.write(json.dumps(board))
    f.close()

    print('Backup complete.\n')

def main():
    print_board()

main()
