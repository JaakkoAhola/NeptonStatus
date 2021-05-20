Connect your Nepton status to your FMI Slack status.

Needed environment variables:
* NEPTONMOBILE = your mobile url of nepton
* SLACK_USER_ID = your FMI slack user ID
* SLACK_API_TOKEN_NEPTON_STATUS = slack app OAuth token with users.profile:read and users.profile:write OAuth Scopes

Set the `status_text` and `status_emoji` values to be your liking in `self.statusPool` instance variable in [SlackStatus.py](SlackStatus.py)


Used conda environment given in [slackAPI.yml](slackAPI.yml) (N.B. not very clean environment)
