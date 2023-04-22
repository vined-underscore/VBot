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
        "channel": {
            "webhook_url": ""
        } # Put blank to not log in a channel
    }

    global nitro_sniper; nitro_sniper = {
        "url": "", # Nitro sniper URL
        "snipe": True,
        "ping": True # If to ping @everyone when a code has been sniped
    }
    