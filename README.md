

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
`DEFAULT_FILE_STORAGE`  
: `DEFAULT_FILE_STORAGE=scouts_auth.inuits.files.aws.S3StorageService`  
`USE_S3_STORAGE`  
: If set to True, then the storage backend used will be `scouts_auth.inuits.files.aws.S3StorageService`  
`USE_SEND_IN_BLUE`  
: If set to True, then emails will be sent through SendInBlue



3. EDITING I18N FRONTEND  
In frontend repo: `/src/locales/nl.json`  
- Copy the text in the frontend
- Search for it in the locale file
- Replace with the desired text

4. EDITING FIXTURES  
4.1 Relevant fixtures  
- * CAMP TYPES: `scouts_kampvisum_api/apps/camps/fixtures/camp_types.json`  
  Defines the camp types that can be selected in the frontend and are linked in the categories and sub-categories
- # CAMP YEARS: `scouts_kampvisum_api/apps/camps/fixtures/camp_years.json`  
  Defines the available camp years. If a camp year has not been defined here, it will automatically be created.
- `scouts_kampvisum_api/apps/groups/fixtures/scouts_group_types.json`  
  Defines the different group types (as per GroepAdmin). A parent group type can be defined to further classify a group type.
- `scouts_kampvisum_api/apps/groups/fixtures/scouts_section_names.json`  
  Defines the different standard scouts section names with a name, a gender and an age group (which is the starting age for that section).
- `scouts_kampvisum_api/apps/groups/fixtures/default_scouts_section_names.json`  
  Links the group type with the section name to determine the list of default scouts sections a group has.
- `scouts_kampvisum_api/apps/visums/fixtures/category_set_priorities.json`  
  Determines the precedence of one category set over another. Currently not in use anymore.
- `scouts_kampvisum_api/apps/visums/fixtures/check_types.json`  
  Specifies the different types of checks. DO NOT CHANGE. Changes to this file require change in both back- and front-end. Contact inuits.
- `scouts_kampvisum_api/apps/visums/fixtures/categories.json`  
  Defines the different categories
- `scouts_kampvisum_api/apps/visums/fixtures/sub_categories.json`  
- `scouts_kampvisum_api/apps/visums/fixtures/checks.json`  
- `scouts_kampvisum_api/apps/deadlines/fixtures/default_deadlines.json`  
- `scouts_kampvisum_api/apps/deadlines/fixtures/default_deadline_sets.json`  
- `scouts_kampvisum_api/apps/deadlines/fixtures/camp_registration_deadlines.json`  

