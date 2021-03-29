## Create Account
`create_account = hierarchy.create_account(access_token=access_token, account='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| account| account to create |
### Response Type
Json Response
### Example Usage
`hierarchy = Hierarchy()`\
`create_account = hierarchy.create_account(access_token=access_token, account='')`
## Get Account
`get_account = hierarchy.get_account(access_token=access_token, page='', limit='', key='', my_account='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| page| for pagination |
| key| maximum number of results to return|
| my_account|keyword to search|
|my_account|To get accounts belong to user (super admin)|
### Response Type
Json Response
### Example Usage
`hierarchy = Hierarchy()`\
`get_account = hierarchy.get_account(access_token=access_token, page='', limit='', key='', my_account='')`
## Update Account
`update_account = hierarchy.update_account(access_token=access_token, id='', account='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| id| ID of account |
| account| Account to update in the organization |
### Response Type
Json Response
### Example Usage
`hierarchy = Hierarchy()`\
`update_account = hierarchy.update_account(access_token=access_token, id='', account='')`
## Get Account Settings
`get_account_settings = hierarchy.get_account_settings(access_token=access_token, id='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| id| account_id |
### Response Type
Json Response
### Example Usage
`hierarchy = Hierarchy()`\
`get_account_settings = hierarchy.get_account_settings(access_token=access_token, id='')`
## Update Account Settings
`update_account_settings = hierarchy.update_account_settings(access_token=access_token, id='', accountSetting='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| id| account_id |
| accountSetting| account to create |
### Response Type
Json Response
### Example Usage
`hierarchy = Hierarchy()`\
`update_account_settings = hierarchy.update_account_settings(access_token=access_token, id='', accountSetting='')`
## Get Hierarchy Summary
`get_hierarchy_summary = hierarchy.get_hierarchy_summary(access_token=access_token, account_id='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| account_id| ID of the account |
### Response Type
Json Response
### Example Usage
`hierarchy = Hierarchy()`\
`get_hierarchy_summary = hierarchy.get_hierarchy_summary(access_token=access_token, account_id='')`
## Create Tiers
`create_tiers = hierarchy.create_tiers(access_token=access_token, tier='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| tier| Tier to create |
### Response Type
Json Response
### Example Usage
`hierarchy = Hierarchy()`\
`create_tiers = hierarchy.create_tiers(access_token=access_token, tier='')`
