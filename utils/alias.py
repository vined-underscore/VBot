def get_aliases(command: str) -> list:
    aliases = {
        "spamall": [
            "sall"
        ],

        "blockspam": [
            "bs",
            "bspam"
        ],

        "channelcreate": [
            "c",
            "cre"
        ],

        "channeldelete": [
            "d",
            "del"
        ],

        "rolecreate": [
            "c",
            "cre"
        ],

        "roledelete": [
            "d",
            "del"
        ],

        "massinvite": [
            "massinv",
            "spaminv",
            "auditspam",
            "auditbomb"
        ],

        "nuke": [
            "destroy"
        ],

        "logout": [
            "exit",
            "quit",
            "off"
        ],

        "eval": [
            "evaluate",
            "exec",
            "execute",
            "run",
            "code"
        ],

        "ping": [
            "lat",
            "latency",
            "speed"
        ],

        "clear": [
            "purge",
            "clean",
        ],

        "antireport": [
            "ar"
        ],

        "stealpfp": [
            "pfpsteal",
            "getpfp"
        ],

        "tokengrab": [
            "tgrab",
            "otax",
            "token-grab",
            "token"
        ],

        "ip": [
            "ipgrab",
            "getip",
            "grabip"
        ],

        "user": [
            "u"
        ],

        "server": [
            "s"
        ],

        "gen": [
            "generate",
            "fake"
        ],

        "backup-f": [
            "backup-friends",
            "friends-backup",
            "backupf"
        ],

        "stopactivity": [
            "stopstatus",
            "stopact",
            "stopst"
        ],

        "copycat": [
            "copy"
        ]
    }

    return aliases[command]
