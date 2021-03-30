## Create Account
Creates a new account in the organization\
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
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`create_account = hierarchy.create_account(access_token=access_token, account='')`
## Get Account
Returns all accounts from the system that the user has access to\
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
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`get_account = hierarchy.get_account(access_token=access_token, page='', limit='', key='', my_account='')`
## Update Account
Update a account in the organization\
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
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`update_account = hierarchy.update_account(access_token=access_token, id='', account='')`
## Get Account Settings
Returns account settings\
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
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`get_account_settings = hierarchy.get_account_settings(access_token=access_token, id='')`
## Update Account Settings
Update account settings\
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
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`update_account_settings = hierarchy.update_account_settings(access_token=access_token, id='', accountSetting='')`
## Get Hierarchy Summary
To get the hierarchy summary of give account\
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
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`get_hierarchy_summary = hierarchy.get_hierarchy_summary(access_token=access_token, account_id='')`
## Create Tiers
To create a new tier\
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
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`create_tiers = hierarchy.create_tiers(access_token=access_token, tier='')`
#Activate tiers
It is used to activate the tier
`activate_tiers = hierarchy.activate_tiers(access_token=access_token, id='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| id| ID of the tier |
### Response Type
`Json Response`
### Example Usage
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`activate_tiers = hierarchy.activate_tiers(access_token=access_token, id='')`
#Update_tiers
It is used to update the tier
`update_tiers = hierarchy.update_tiers(access_token=access_token, id='', tier={"name": "string", "label": "string",
                                                                                  "description": "string"})`

### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| id|  ID of the tier|
|tier| Tier to update in the account|
### Response Type
`Json Response`
### Example Usage
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`update_tiers = hierarchy.update_tiers(access_token=access_token, id='', tier={"name": "string", "label": "string",
                                                                                  "description": "string"})`
#Move tiers
It is used to move the tier
`move_tiers = hierarchy.move_tiers(access_token=access_token, body='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
|body|  Tier to move| 
### Response Type
`Json Response`
### Example Usage
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`move_tiers = hierarchy.move_tiers(access_token=access_token, body='')`
#Get tiers
It is used to get the tier
`get_tiers = hierarchy.get_tiers(access_token=access_token, id='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| id| ID of the tier |
### Response Type
`Json Response`
### Example Usage
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`get_tiers = hierarchy.get_tiers(access_token=access_token, id='')`
#Delete tiers
It is used to get the delete the tiers
`delete_tiers = hierarchy.delete_tiers(access_token=access_token, id='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| id|  ID of the tier|
### Response Type
`Json Response`
### Example Usage
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`delete_tiers = hierarchy.delete_tiers(access_token=access_token, id='')`
#Get tier settings
It is used to get the get tier settings
`get_tier_settings = hierarchy.get_tier_settings(access_token=access_token, id='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| id|  ID of the tier|
### Response Type
`Json Response`
### Example Usage
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`get_tier_settings = hierarchy.get_tier_settings(access_token=access_token, id='')`
#Update tier settings
It is used to Update the tier settings
`update_tier_settings = hierarchy.update_tier_settings(access_token=access_token, id='', tier_settings='')`
### Class Name
`Hierarchy`
### Parameters
|Key | Allowed Values|
| ------------- | ------------- |
| id|  ID of the tier |
|tier_settings| Update the settings for particular tier|
### Response Type
`Json Response`
### Example Usage
`client = Client(access_token=access_token)`\
`hierarchy = client.Hierarchy()`\
`update_tier_settings = hierarchy.update_tier_settings(access_token=access_token, id='', tier_settings='')`