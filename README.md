# JustAnotherGroupBot

Bot to manage Telegram groups. Nothing fancy. So far it is in Italian only.

This was an exercize in utilizing the Telegram bot API and API endpoints, so to give myself a greater challenge.
I had some rough limitations, such as not being able to list the users in a group chat; that is why you will need to fill out the chat members dictionary by hand, in JSON. Sorry. 

The expected format for the JSON is as following:

```
{
    "users" :
    [
        {
            "id" : # insert here the user's Telegram account ID + ,
            "user" : # insert here the user's handle (with the '@' included) 
        },

        # etc...
    ]
}
```

The available commands are as following: 

- /start, to start the bot (wow)
- /echo <your message>, to make the bot say something
- /ban @user, to remove a user from the group chat (only works with the users listed in chatmembers.json)
- /unban @user, to reinstate a user from the group chat (only works with the users listed in chatmembers.json)
- /kick @user, to kick a user from the group chat (limitations as above)

So far, there aren't many things this bot can do. I know.

To configure your instance, you have to:

- open the Python interpreter in the folder where the files are downloaded
- run `python -r requirements.txt` to install all dependencies
- create botToken.txt and copypaste your bot token in there
- create and fill out chatmembers.json as explained before (one day I'll use SQL...)
- start the bot with `python start.py` 
- enjoy (I hope!)

You are welcomed to report issues, this is still a WIP :)
