# Games For Love - Tech Code Repository

## Overview
This is the code for to run an automated outreach bot on Twitter. The rest of this documention will cover various features, code breakdown, and future steps.

## Airtable Data

The script depends on the name and format of the ```Twitch Top 400- Ranked & Scored``` table. If you want to rename the table, change the corresponding variable in the .env file (variable ```INFLUENCERS_TABLE_NAME```).

Do NOT change the names and the format of the following fields:
- Name
- Twitter Handle (Twitter handle of streamer)
- Ranking (compatibility ranking of 0-4, if 0, bot won’t send the message to this influencer) 
- Twitter DM blocked? (whether the streamers DM’s are off)
- Last Twitter message attempt (when the last message was sent to streamer)
- Number of attempts (number of messages sent so far, must have a value, 0 by default)
- Expressed interested (checked if influencer expressed interest in partnering with GFL)
- Opt-out (checked if influencer asked to stop sending messages to them)
- Errors (any errors that occur when running system)
- recipient_id (information needed for checking received messages)


### Modifying Outreach Messages
The ```Twitter Bot Parameters``` table, there are options to change the number of messages to send, the frequency, and the content of each message itself. It is suggested to insert any new code parameters/variable into this specific table, to keep all parameters in one place.

## Code Overview

### Key Features
Lorem ipsum

### Files
#### twitter.py
The main python file to create and set-up the Twitter bot and connect data to Airtable. Contains definition and implementation of TwitterBot class. The most important method of this class is called send_dm. It is the place where the bulk of the work happens. send_dm checks all the conditions and parameters from Airtable and based on the logic implemented there sends a message to the influencer. If you want to change any behaviour, that's place to look at.

#### .secrets
File containing API keys and token to enable accessing Twitter and Airtable services.

#### .env
File containing environmental variables.

#### requirements.txt
Consolidated .txt document of all plugins/libraries required for the script to run efficiently.
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

## Running & Deploying the Script

### Local Development
In order to run this code locally, clone this repository using ```git clone``` command, then create a virtual environment in the same folder using Python’s ```venv``` module (optional), and finally install all necessary dependencies using ```pip install -r requirements.txt```


## Potential Difficulties/Future Steps
 - Users with DMs blocked will not receive messages. However, this will be indicated in the Airtable and GFL can manually reach out or use another platform.
 - The hosting service has time and/or usage limitations.
 - There are opportunities to expand this bot to utilize other outreach platforms such as Twitch and Discord, using similar features and code structure.
    - Refer to the Platform Overview Report for a more comprehensive summary.
 - There are opportunities to expand the functionality of the Twitter bot, such as NLP to reply with tailored automated messages.
