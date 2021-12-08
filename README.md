# Games For Love - Tech Code Repository

## Overview
This is the code for to run an automated outreach bot on Twitter. The rest of this documention will cover various features, code breakdown, and future steps.

## Airtable Data

The script depends on the name and format of the ```Twitch Top 400- Ranked & Scored``` table. If you want to rename the table, change the corresponding variable in the .env file (variable ```INFLUENCERS_TABLE_NAME```).

Do NOT change the names and the format of the following fields:
- Name
- Twitter Handle (Twitter handle of streamer)
- Ranking (compatibility ranking of 0-4) 
- Twitter DM blocked? (whether the streamers DM’s are off)
- Last Twitter message attempt (when the last message was sent to streamer)
- Number of attempts (number of messages sent so far)
- Errors (any errors that occur when running system)

### Modifying Outreach Messages
The ```Twitter Bot Parameters``` table, there are options to change the number of messages to send, the frequency, and the content of each message itself. It is suggested to insert any new code parameters/variable into this specific table, to keep all parameters in one place.

## Code Overview

### twitter.py
Purpose: Send messages to streamers through twitter in mass

Takes data inputed to the airtable and uses information to deliver message
### main.py
Purpose: update the airtable after DM is sent

### Code Setup Requirements
```
certifi==2021.10.8
charset-normalizer==2.0.7
idna==3.3
oauthlib==3.1.1
pyairtable==1.0.0.post1
python-dotenv==0.19.1
requests==2.26.0
requests-oauthlib==1.3.0
tweepy==4.3.0
urllib3==1.26.7
```

### POTENTIAL DIFFICULTIES/FUTURE STEPS
#Users with DMs blocked will not receive messages
#Hosting the service has limitations
#There are opportunities to expand this bot to utilize other outreach platforms such as twitch and discord.
#There are opportunities to expand the functionality of the twitter bot.
