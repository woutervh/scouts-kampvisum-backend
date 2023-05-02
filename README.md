
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
- createdeadlinesets  

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
   - If you do specify an index to explicitly order the object, then you will have to set it on all objects yourself.  
   - Adding categories, sub-categories or checks is equally easy. Be sure to correctly specify the parent.  
   - Most of the fixtures are rewritten in the background by the appropriate command to provide extra data or link to dependent models.  
   - JSON is unforgiving for syntax errors and very strict on spacing. Follow the rules as evident from the existing fixtures when editing.  
   - See below for examples (3 and further). If a field is optional and omitted, the default value will be silently set.  
   - It is probably best practice to edit fixtures in the appropriate order. For instance: to add a check, you will need the sub-category and category.  If any of those need to be defined, start with them. The order would thus be: edit categories, edit sub-categories, edit checks.  
     Similar for deadlines, you will probably define deadlines that are linked to a sub-category or check. Define them first, then add the deadline.  
     This will avoid certain types of headaches.  
2. Naming conventions:
   - Django fixtures are not intended for the usage described here. They load initial data, with the primary key specified. In the case of integer primary keys, this may be more or less manageable, but with the current implementation of uuid keys, declaring the parent sub-category for a check would be a major pain.  
     The parents are therefore specified by their natural keys, i.e. the combination of keys that uniquely identify a parent.  
     This makes for more typing, but dramatically increases readability and thus reduces errors.  
   - This loading by natural keys can however also become difficult if not following a strict naming convention.  
   - The names of the objects does not need to be unique (only their natural key combination), but it is highly recommended to give every object a unique name nonetheless.
   - Choose whatever naming convention you like, but make your life easier by using a logical rule and following it strictly.  
   - The convention used by inuits is this (all objects have a unique name):  
     **categories**: an all lowercase easy name for the category,  
     e.g. `planning`  
     **sub-categories**: an all lowercase, easy name for the sub-category, preceded by the name of the category and an underscore,  
     e.g. `planning_date`  
     **checks**: an all lowercase, ease name for the check, preceded by the name of the sub-category and an underscore, preceded by the name of the category and an underscore  
     e.g. `planning_date_members`  
3. Examples: Category  
   - Fixture: `apps/visums/fixtures/categories.json`  
   - Fields:  
     - **`name`** (**REQUIRED**):  
       The category name  
       It is recommended to make this a more machine readable identifier, in all lowercase, e.g. "logistics_locations"  
     - **`camp_year`** (**OPTIONAL**, default: _the current camp year_):  
       The scouts year for which the category is defined  
     - **`camp_types`** (**OPTIONAL**, default: _all camp types except "basis"_):  
       An array of camp types for which the category should be set  
       An expander camp type is available: *****, this is equivalent to specifying all the camp types, except "basis".  
       Be sure not to include the "basis" camp type when specifying other camp types, because then the category will be doubled in the visum.  
       If in doubt, your best bet is to set this to "basis".  
     - **`label`** (**OPTIONAL**, default: _""_):  
       A human readable name for the category that will be displayed in the frontend, e.g. "Logistiek"  
     - **`description`** (**OPTIONAL**, default: _""_):  
       Currently unused for categories.
     - **`explanation`** (**OPTIONAL**, default: _""_):  
       Provides an explanation of what the category is about that is shown in the info sidebar. Can contain HTML links.
     - **`index`** (**OPTIONAL**, default: _a value calculated on the order of appearance in the fixture_):  
       Determines the ordering of the category when returned from the db and thus where it shows up in the frontend.  
       If set for one category, it should be set correctly for all other categories.  
     - **`priority`** (**OPTIONAL**, default: _Verbond_):  
       A remainder from a previous implementation iteration, but kept on the model to ease the integration of possible future changes. This determines a hierarchy of authority in the category definition. A category with a priority of "Verbond" will always have precedence over a category with the priority "Groep"  
 
4. Examples: SubCategory  
   - Fixture: `apps/visums/fixtures/sub_categories.json`  
   - Fields:  
     - **`name`** (**REQUIRED**):  
       The sub-category name  
       It is recommended to make this a more machine readable identifier, in all lowercase and preceded by the name of the category and an underscore, e.g. "logistics_locations"  
     - **`category`** (**REQUIRED**):  
       The parent sub_category, defined as follows:  
       ```
       "category": [
        "<name of the parent category>",
        <camp_year_ of the parent category>
       ]
       ```
       For example:
       ```
       "category": [,
        "logistics",
        2022
       ]  
     - **`camp_types`** (**OPTIONAL**, default: _all camp types except "basis"_):  
       An array of camp types for which the sub-category should be set  
       An expander camp type is available: *****, this is equivalent to specifying all the camp types, except "basis".  
       Be sure not to include the "basis" camp type when specifying other camp types, because then the sub-category will be doubled in the visum.  
       If in doubt, your best bet is to set this to "basis".  
     - **`label`** (**OPTIONAL**, default: _""_):  
       A human readable name for the sub-category that will be displayed in the frontend, e.g. "Locaties"  
     - **`description`** (**OPTIONAL**, default _""_):  
       Currently unused.
     - **`explanation`** (**OPTIONAL**, default: _""_):  
       Provides an explanation of what the check is about that is shown in the info sidebar. Can contain HTML links.  
       If present, an information icon will be shown next to the check name that will open the info sidebar.
     - **`index`** (**OPTIONAL**, default: _a value calculated on the order of appearance in the fixture_):  
       Determines the ordering of the check when returned from the db and thus where it shows up in the frontend.  
       If set for one check, it should be set correctly for all other checks.  
     - **`link`** (**OPTIONAL**, default: _""_):  
       A remainder from a previous implementation iteration, but kept for possible future changes. This could set a hyperlink on the check label for instance. Currently unused.
       Use HTML links in the explanation to provide links to external resources.
5. Examples: Check  
   - Fixture: `apps/visums/fixtures/checks.json`  
   - Fields:  
     - **`name`** (**REQUIRED**):  
       The check name  
       It is recommended to make this a more machine readable identifier, with all lowercase and underscores in stead of spaces, e.g. "logistics_locations"  
     - **`sub_category`** (**REQUIRED**):  
       The parent sub_category, defined as follows:  
       ```
       "sub_category": [
        "<name of the parent sub-category>",
        [
          "<name of the parent category>",
          <camp_year_ of the parent category>
        ]
       ]
       ```
       For example:
       ```
       "sub_category": [
         "logistics_locations",
         [
          "logistics",
          2022
         ]
       ]
     - **`check_type`** (**REQUIRED**):  
       An important one. Determines the type of check. See below for a list of all available check types.
     - **`label`** (**OPTIONAL**, default: _""_):  
       A human readable name for the sub-category that will be displayed in the frontend, e.g. "Locaties"  
     - **`description`** (**OPTIONAL**, default _""_):  
       Currently unused.
     - **`explanation`** (**OPTIONAL**, default: _""_):  
       Provides an explanation of what the check is about that is shown in the info sidebar. Can contain HTML links.  
       If present, an information icon will be shown next to the check name that will open the info sidebar.
     - **`index`** (**OPTIONAL**, default: _a value calculated on the order of appearance in the fixture_):  
       Determines the ordering of the check when returned from the db and thus where it shows up in the frontend.  
       If set for one check, it should be set correctly for all other checks.  
     - **`link`** (**OPTIONAL**, default: _""_):  
       A remainder from a previous implementation iteration, but kept for possible future changes. This could set a hyperlink on the check label for instance. Currently unused.
       Use HTML links in the explanation to provide links to external resources.
     - **`change_handlers`** (**OPTIONAL**, default: _["default_check_changed"]_)
       Should not be defined by users as it refers to methods in the class `ChangeHandlerService` (`apps/visums/services/change_handler_service.py`) and will cause an error if it refers to a non-existent method.
       This is used to trigger further actions when a check is changed.
       Currently only used for the camp responsible check, since it may require emails to be sent.
       The value defined in `settings.CHECK_CHANGED` is always added to the change_handlers.
     - **`is_multiple`** (**OPTIONAL**, default: false)
       A boolean that determines if the check allows for a single instance to be added, or multiple.
       Mainly used for the different participant checks, where they determine if the check sets a single or a list of particpants.
     - **`is_member`** (**OPTIONAL**, default: false)
       A remainder from a previous implementation iteration, but kept on the model to ease the integration of possible future changes.
       This was used to limit the types of people that were allowed to be set on the participant check. Currently useless, because all different participant types are captured in their proper check type.
     - **`is_required_for_validation`** (**OPTIONAL**, default: true)
       A boolean that determines if the check needs to have a value set to validate as CheckState.CHECKED.

3. Check types  
   Defined in file `apps/visums/fixtures/check_types.json`
   - **SimpleCheck**  
     A check that can be checked, unchecked or set as not applicable  
   - **DateCheck**  
     A check that contains a date  
     Currently unused.  
   - **DurationCheck**  
     A check that contains a start and end date  
   - **LocationCheck**  
     A check that contains one or more geo-coordinates  
   - **CampLocationCheck**  
     A check that contains one or more geo-coordinates and contact details  
   - **ParticipantCheck**  
		 A check that selects members and non-members  
   - **ParticipantMemberCheck**  
     A check that selects members  
   - **ParticipantCookCheck**  
     A check that selects cooks
   - **ParticipantLeaderCheck**  
     A check that selects leaders  
   - **ParticipantResponsibleCheck**  
     A check that selects camp responsibles  
   - **ParticipantAdultCheck**  
     A check that selects 21-year-olds  
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
  12. **DEADLINES:**  
      - FIXTURE: `scouts_kampvisum_api/apps/deadlines/fixtures/deadlines.json`  
      - COMMAND: `django-manage.py loaddefaultdeadlines`  
      - Defines LinkedSubCategory, LinkedChecked and plain deadlines.  
  13. **CAMP REGISTRATION DEADLINE:**  
      - FIXTURE: `scouts_kampvisum_api/apps/deadlines/fixtures/camp_registration_deadlines.json` 
      - COMMAND: `django-manage.py loaddefaultdeadlines`  
      - Defines the deadlines that apply for the custom camp registration deadline.  
  14. **DEADLINE SETS:**  
      - FIXTURE: `scouts_kampvisum_api/apps/deadlines/fixtures/deadline_sets.json`  
      - COMMAND: `django-manage.py createdeadlinesets`  
      - Bundles deadlines into sets for a particular camp year and camp types.  

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

2. **`insomnia`**  
   Sets up test data and returns a dict of uuid's to use in insomnia.  
   This command should only be ran in a development environment, as it makes some changes to the db.  
