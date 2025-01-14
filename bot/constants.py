'''
Change the variables to whatever your server IDs are. Each is labelled accordingly
'''

WELCOME_CHANNEL_ID = 1011049173442895902 # Replace with the actual ID of your welcome text channel

VERIFIED_MEMBER_ID = 1120501110407434301 # Replace with the actual ID of the role you want for the greetings message

WELCOME_REACT_EMOJI = "👍" # Replace with the emoji you want to use for your welcome message react emoji

AUTO_MOVE_FLAG = True # REQUIRED: If you want to use the auto move ability for RasenBot then set to True. If not then set to False

DIFFERENT_NAME_CHANNELS = { # REQUIRED IF USING AUTO MOVE: If you are using auto move you must have lounge, study, cinema, and general channels. You can name them whatever you want but make sure to replace the channel IDs with your server's
    "Lounge": 1132567562014691418,
    "Study": 1131758538566410301,
    "Cinema": 1131758561249218620,
    "General": 989667924291772482,
}