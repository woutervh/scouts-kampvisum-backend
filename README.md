

# Welcome to the kampvisum app


## Installation

1. ENV: DEVELOPMENT @ INUITS  
`git clone ssh://git@gitlab.inuits.io:2224/customers/scouts/kampvisum/scouts-kampvisum-docker.git docker`  
`cd docker`  
`./init_project.sh`  

2. ENV: ACCEPTANCE @ SCOUTS  
2.1. Noteable settings:  
`ACTIVITY_EPOCH`  
:  Default 0 for limitless. A setting that determines (in number of years) when a member is considered inactive after the last active function.  
This is used for instance in filtering member searches on the groupadmin.  
`CAMP_REGISTRATION_EPOCH`  
:  Default 05-01 (MM-DD). A setting that determines when in the course of the year a newly registered camp should be considered to be part of the next camp year, instead of the current one.  
`RESPONSIBILITY_EPOCH`
:  Default 04-01 (MM-DD). A setting that determines when the camp responsibles have to take extra action if a responsible person changes.
`IS_ACCEPTANCE`  
:  If True and DEBUG=True, then emails will be sent to the debug address.  
`DEBUG`  
`LOGGING_LEVEL`  
: Determines the level of logging for all django apps.  
`LOGGING_LEVEL_ROOT`  
: Determines the level of logging for django's own logging.  

`DEFAULT_FILE_STORAGE=scouts_auth.inuits.files.aws.S3StorageService`  
USE_S3_STORAGE`  
: If set to True, then the storage backend used will be `scouts_auth.inuits.files.aws.S3StorageService`  

USE_SEND_IN_BLUE  