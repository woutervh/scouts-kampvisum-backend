

# **Welcome to the kampvisum app**  


## **INSTALLATION**  
   1. REDMINE/GITLAB/DOCS
      - redmine: [https://redmine.inuits.eu/projects/scouts-kampvisum](https://redmine.inuits.eu/projects/scouts-kampvisum)   
      - gitlab: [https://gitlab.inuits.io/customers/scouts/kampvisum](https://gitlab.inuits.io/customers/scouts/kampvisum)  
      - figma: [https://www.figma.com/file/S4I8apCFM0fTOujABx6hEr/](https://www.figma.com/file/S4I8apCFM0fTOujABx6hEr/)  
      - trello kampkaft: [https://trello.com/b/KBqpuKw5/](https://trello.com/b/KBqpuKw5/)  
      - trello kampkaft buitenlandse kampen: [https://trello.com/b/KBqpuKw5/](https://trello.com/b/KBqpuKw5/)  
   2. GIT  
      - [BACKEND](https://gitlab.inuits.io/customers/scouts/kampvisum/scouts-kampvisum-api): `ssh://git@gitlab.inuits.io:2224/customers/scouts/kampvisum/scouts-kampvisum-api.git`  
      - [BACKEND SCOUTS](https://github.com/ScoutsGidsenVL/kampvisum-backend): `git@github.com:ScoutsGidsenVL/kampvisum-backend.git`  
      - [FRONTEND](https://gitlab.inuits.io/customers/scouts/kampvisum/scouts-kampvisum-frontend): `ssh://git@gitlab.inuits.io:2224/customers/scouts/kampvisum/scouts-kampvisum-frontend.git`  
      - [FRONTEND SCOUTS](https://github.com/ScoutsGidsenVL/kampvisum-frontend): `git@github.com:ScoutsGidsenVL/kampvisum-frontend.git`  
      - [DOCKER](https://gitlab.inuits.io/customers/scouts/kampvisum/scouts-kampvisum-docker): `ssh://git@gitlab.inuits.io:2224/customers/scouts/kampvisum/scouts-kampvisum-docker.git`  

      The `init_project.sh` script mentioned in the next paragraph will clone and setup remotes for you.  

   3. DEVELOPMENT ENVIRONMENT @ INUITS  
      - `git clone ssh://git@gitlab.inuits.io:2224/customers/scouts/kampvisum/scouts-kampvisum-docker.git docker`  
      - `cd docker`  
      - `./init_project.sh`  


## **SETUP**  

Most of the time, a simple `django_manage.py migrate` should be sufficient to create and run migrations.  
If this should fail, there is a script that specifically makes and runs migrations for every app:  
`scripts/migrations.sh`

For setup through other means, the following commands should be run, in the following order and after `migrate`:  
- runfixtures
- setupcampyears
- loadcategories
- loadsubcategories
- loadchecks
- createcategorysets
- loaddefaultdeadlines
- createdefaultdeadlinesets  

## **SETTINGS**  
   - `ACTIVITY_EPOCH`  
     Default 0 for limitless. A setting that determines (in number of years) when a member is considered inactive after the last active function.  
     This is used for instance in filtering member searches on the groupadmin.  
   - `CAMP_REGISTRATION_EPOCH`  
     Default 05-01 (MM-DD). A setting that determines when in the course of the year a newly registered camp should be considered to be part of the next camp year, instead of the current one.  
   - `RESPONSIBILITY_EPOCH`
     Default 04-01 (MM-DD). A setting that determines when the camp responsibles have to take extra action if a responsible person changes.
   - `IS_ACCEPTANCE`  
     If True and DEBUG=True, then emails will be sent to the debug address.  
   - `DEBUG`  
   - `LOGGING_LEVEL`  
     Determines the level of logging for all apps.  
   - `LOGGING_LEVEL_ROOT`  
     Determines the level of logging for django's own logging.  
   - `DEFAULT_FILE_STORAGE`  
   - `DEFAULT_FILE_STORAGE=scouts_auth.inuits.files.aws.S3StorageService`  
   - `USE_S3_STORAGE`  
   - If set to True, then the storage backend used will be `scouts_auth.inuits.files.aws.S3StorageService`  
   - `USE_SEND_IN_BLUE`  
     If set to True, then emails will be sent through SendInBlue

## **EDITING i18N (FRONTEND)**  
In frontend repo: `/src/locales/nl.json`  
- Copy the text in the frontend
- Search for it in the locale file
- Replace with the desired text
- GITHUB: If editing through the github interface: click 'commit changes', otherwise:
- GIT:
  * `git add src/locales/nl.json`
  * `git commit -m "a sensible commit message that accurately reflects the changes"`
  * `git push origin master`

## **EDITING FIXTURES**
1. General rules
   - The fixtures should be loaded by running the appropriate command, either `runfixtures` or a fixture-specific command such as `loadcategories`.
   - A custom command (`updatevisums`) is provided to facilitate editing the category, sub-category and check fixtures. This command will reload
     the category, sub-category and check fixtures, setup category sets and then check that existing visums are updated, thus avoiding the error-prone
     procedure of calling the correct commands in the correct order.
   - Categories, sub-categories and checks are ordered according to their location in the fixture.  
     If you change an item's position in the fixture and run the appropriate command, the occurrence in the frontend will change accordingly.  
   - Adding categories, sub-categories or checks is equally easy. Be sure to correctly specify the parent


2. Check types
   - **SimpleCheck**  
     A check that can be checked, unchecked or set as not applicable  
   - **DateCheck**  
     A check that contains a date  
   - **DurationCheck**  
     A check that contains a start and end date  
   - **LocationCheck**  
     A check that contains one or more geo-coordinates  
   - **CampLocationCheck**  
     A check that contains one or more geo-coordinates and contact details  
   - **ParticipantCheck**  
     A check that selects members and non-members  
   - **FileUploadCheck**  
     A check that contains a file  
   - **CommentCheck**  
     A check that contains comments  
   - **NumberCheck**  
     A check that contains numbers  

## **FIXTURES**  
  1. **CAMP TYPES:**  
     - FIXTURE: `scouts_kampvisum_api/apps/camps/fixtures/camp_types.json`  
     - COMMAND: `django-manage.py runfixtures`  
     - Defines the camp types that can be selected in the frontend and are linked in the categories and sub-categories.  
  2. **CAMP YEARS:**  
      - FIXTURE: `scouts_kampvisum_api/apps/camps/fixtures/camp_years.json`  
      - COMMAND: `django-manage.py setupcampyears`  
      - Defines the available camp years. If a camp year has not been defined here, it will automatically be created.  
  3. **SCOUTS GROUP TYPES:**  
      - FIXTURE: `scouts_kampvisum_api/apps/groups/fixtures/scouts_group_types.json`  
      - COMMAND: `django-manage.py runfixtures`  
      - Defines the different group types (as per GroepAdmin). A parent group type can be defined to further classify a group type.  
  4. **SCOUTS SECTION NAMES:**  
      - FIXTURE: `scouts_kampvisum_api/apps/groups/fixtures/scouts_section_names.json`  
      - COMMAND: `django-manage.py runfixtures`  
      - Defines the different standard scouts section names with a name, a gender and an age group (which is the starting age for that section).  
  5. **DEFAULT SCOUTS SECTIONS:**  
      - FIXTURE: `scouts_kampvisum_api/apps/groups/fixtures/default_scouts_section_names.json`  
      - COMMAND: `django-manage.py runfixtures`  
      - Links the group type with the section name to determine the list of default scouts sections a group has.  
  6. **CATEGORY SET PRIORITIES:**  
      - FIXTURE: `scouts_kampvisum_api/apps/visums/fixtures/category_priorities.json`  
      - COMMAND: `django-manage.py runfixtures`  
      - Determines the precedence of one category set over another. Currently not in use anymore.  
  7. **CHECK TYPES:**  
      - FIXTURE: `scouts_kampvisum_api/apps/visums/fixtures/check_types.json`  
      - COMMAND: `django-manage.py runfixtures`  
      - Specifies the different types of checks. DO NOT CHANGE. Changes to this file require change in both back- and front-end. Contact inuits.  
  8. **CATEGORIES:**  
      - FIXTURE: `scouts_kampvisum_api/apps/visums/fixtures/categories.json`  
      - COMMAND: `django-manage.py loadcategories`  
      - Defines the different categories that apply for the given camp types.  
  9. **SUB-CATEGORIES:**  
      - FIXTURE: `scouts_kampvisum_api/apps/visums/fixtures/sub_categories.json`  
      - COMMAND: `django-manage.py loadsubcategories`  
      - Defines the sub-categories that are linked to categories.  
  10. **CHECKS:**  
      - FIXTURE: `scouts_kampvisum_api/apps/visums/fixtures/checks.json`  
      - COMMAND: `django-manage.py loadchecks`  
      - Defines the checks that are linked to sub-categories.  
  12. **DEFAULT DEADLINES:**  
      - FIXTURE: `scouts_kampvisum_api/apps/deadlines/fixtures/default_deadlines.json`  
      - COMMAND: `django-manage.py loaddefaultdeadlines`  
      - Defines LinkedSubCategory, LinkedChecked and plain deadlines.  
  13. **CAMP REGISTRATION DEADLINE:**  
      - FIXTURE: `scouts_kampvisum_api/apps/deadlines/fixtures/camp_registration_deadlines.json` 
      - COMMAND: `django-manage.py loaddefaultdeadlines`  
      - Defines the default deadlines that apply for the custom camp registration deadline.  
  14. **DEFAULT DEADLINE SETS:**  
      - FIXTURE: `scouts_kampvisum_api/apps/deadlines/fixtures/default_deadline_sets.json`  
      - COMMAND: `django-manage.py createdefaultdeadlinesets`  
      - Bundles default deadlines into sets for a particular camp year and camp types.  

## **COMMANDS**  


1. **`runfixtures`**  
   Uses django's loaddata command to load the following fixtures (in order):  
   - groups/fixtures/scouts_group_types.json
   - groups/fixtures/scouts_section_names.json
   - groups/fixtures/default_scouts_section_names.json
   - camps/fixtures/camp_types.json
   - visums/fixtures/category_priorities.json
   - visums/fixtures/check_types.json



      11. **CATEGORY SETS:**  
          - COMMAND: `django-manage.py createcategorysets`  
          - Links the categories, camp types and camp year into category sets.  