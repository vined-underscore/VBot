class config:
    global token; token = "" # Your account token
    global prefix; prefix = [
        "v.",
        ",",
        ">"
    ] # List of prefixes. Can be one or multiple
    
    global logging; logging = {
        "is_logging": True, # Logs stuff like server joins, leaves, commands
        "error_logging": "both", # Error logging. Can be either "console" or "channel" or "both" or "" if you want there to be no error logging (bad idea)
        "url": ""
        # Disable webhooks by changing it to ""
    }

    # You can disable any of the webhooks by changing the URL to ""
    global snipers; snipers = {
        "nitro_sniper": {
            "enabled": False,
            "url": "", # Nitro sniper URL
            "ping": True # If to ping @everyone when a code has been sniped
        },
        "invite_sniper": {
            "enabled": True,
            "url": "", # Invite sniper URL
            "ping": False # If to ping @everyone when an invite has been found
        },
        "keyword_sniper": {
            "enabled": True, # If to log keywords
            "url": "", # Keyword sniper URL
            "ping": True, # If to ping @everyone when a keyword has been found
            
            "keywords": [
                "keyword 1",
                "keyword 2",
                "keyword 3"
            ], # List of keywords to look out for
        }
    }
    