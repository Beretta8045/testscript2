#This Script looks at all users from the database and creates a folder called "Verified" in their mailbox if it doesn't already exist
#This script is designed to run on a schedule to check for new users and create folders for them
#Author: Andy Castro
#andy@nopass.ai

#importing libraries
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError
import json
import urllib.request
import urllib.parse
import requests
import hashlib
from pymongo import MongoClient
import csv
import os
import datetime
import pymongo

#mongo db connection info
client= pymongo.MongoClient("localhost",27017)
gtgdb=client["gtgdb"]
user_collection = gtgdb["user_collection"]

# Function to get secrets from Azure Key Vault
def get_secret(secret_name):
    # The Azure Key Vault URL
    keyvault_url = "https://gtgkeyvault1.vault.azure.net/"

    try:
        # Create a SecretClient using the DefaultAzureCredential
        secret_client = SecretClient(vault_url=keyvault_url, credential=DefaultAzureCredential())
        # Name of the secret to retrieve
        secret_variable  = secret_name

        # Get the secret from the Key Vault
        secret = secret_client.get_secret(secret_variable)

        # Extract the secret value
        secret_value = secret.value
    except ResourceNotFoundError:  
        print("Secret not found")
        secret_value = None
    return secret_value

## Register an Azure Active Directory application with the 'SecurityEvents.ReadWrite.All' Microsoft Graph Permission.
## Get your Azure AD tenant administrator to grant administration consent to your application. This is a one-time activity unless permissions change for the application. 
##Remove for prod 
client_id = get_secret('clientid')

## The appSecret value is a one-time generated value that is displayed upon App Registration and cannot be retrieved without regenerating.
client_secret = get_secret('clientsecret')
tenantId = get_secret('tenantID')
# Azure Active Directory token endpoint.
url = "https://login.microsoftonline.com/%s/oauth2/v2.0/token" % (tenantId)
body = {
    'client_id' : client_id,
    'client_secret' : client_secret,
    'grant_type' : 'client_credentials',
    'scope': 'https://graph.microsoft.com/.default'
}

## authenticate and obtain AAD Token for future calls
data = urllib.parse.urlencode(body).encode("utf-8") # encodes the data into a 'x-www-form-urlencoded' type
req = urllib.request.Request(url, data)

response = urllib.request.urlopen(req)

jsonResponse = json.loads(response.read().decode())

# Grab the token from the response then store it in the headers dict.
aadToken = jsonResponse["access_token"]
headers = { 
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'Authorization' : "Bearer " + aadToken
}
if len(aadToken) > 0:
    print("Access token acquired.")

# Function to create a folder named "Verified" for a user
def read_mongodb_to_list(database_name, collection_name):
    import pymongo
    """
    Reads data from a MongoDB collection and converts it into a list of dictionaries.
    
    Args:
        database_name (str): The name of the MongoDB database.
        collection_name (str): The name of the MongoDB collection.
        
    Returns:
        list: List of dictionaries, each representing a document in the collection.
    """
    # Create a MongoClient instance
    client = pymongo.MongoClient("localhost", 27017)  # Update with your MongoDB connection URL

    # Access the specified database and collection
    db = database_name
    collection = collection_name

    # Retrieve data from the collection and convert it to a list of dictionaries
    data_list = list(collection.find())

    # Close the MongoDB connection
    client.close()

    return data_list

# Function to create a folder named "Verified" for a user
def create_verified_folder(user_id, headers):
    endpoint = "https://graph.microsoft.com/v1.0"
    folder_data = {
        "displayName": "Verified"
    }

    create_folder_url = f'{endpoint}/users/{user_id}/mailFolders'
    create_folder_response = requests.post(create_folder_url, headers=headers, json=folder_data)

    if create_folder_response.status_code == 201:
        folder_id = create_folder_response.json().get('id')
        print(f"Outlook folder 'Verified' created for user ID: {user_id}")
        return folder_id
    elif create_folder_response.status_code == 409:
        # Folder already exists; retrieve its ID
        existing_folder_id = get_verified_folder_id(user_id, headers)
        if existing_folder_id:
            print(f"Outlook folder 'Verified' already exists for user ID: {user_id}")
            return existing_folder_id
        else:
            print(f"Error retrieving existing Outlook folder 'Verified' for user ID: {user_id}")
            return None
    else:
        print(f"Error creating Outlook folder for user ID {user_id}: {create_folder_response.status_code}")
        return None

# Implement the get_verified_folder_id function to retrieve the folder ID in case of a 409 error
def get_verified_folder_id(user_id, headers):
    endpoint = "https://graph.microsoft.com/v1.0"

    # Update the URL to use the specified user_id
    folders_url = f'{endpoint}/users/{user_id}/mailFolders'
    while folders_url:
        folders_response = requests.get(folders_url, headers=headers)
        print(folders_response.json())

        if folders_response.status_code == 200:
            folders_data = folders_response.json()

            # Iterate through the list of folders and find the "Verified" folder
            for folder in folders_data['value']:
                if folder['displayName'] == 'Verified':
                    return folder['id']  # Return the folder ID if found

            # Check if there are more pages
            folders_url = folders_data.get('@odata.nextLink')
        else:
            # Handle the case where there was an error while fetching mailbox folders
            print(f"Error retrieving mailbox folders: {folders_response.status_code}")
            return None

    # If the "Verified" folder does not exist, return None
    return None

def get_user_ids_by_email(email, headers):
    user_ids = {}
    API_ENDPOINT = "https://graph.microsoft.com/v1.0/users"
    params = {
        "$filter": f"userPrincipalName eq '{email}'"
    }

    try:
        response = requests.get(API_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if "value" in data and len(data["value"]) > 0:
            # Extract the user ID from the response
            user_id = data["value"][0]["id"]
        else:
            user_id = None

    except requests.exceptions.RequestException as e:
        print(f"Error while querying Microsoft Graph API: {str(e)}")
        user_id = None

    return user_id

# Function to get all users, create "Verified" folders, and store folder IDs in a dictionary
def main():
    # Replace with your Azure AD access token or authentication headers
    users=read_mongodb_to_list(gtgdb,user_collection)

    # Get the user IDs for each user
    for user in users:
        #check if the user ID is already in the database or if user ID is null
        if user['user_id'] in (None,''):
            # Get the user ID for each user
            user['user_id'] = get_user_ids_by_email(user['email_address'], headers)
            #update the mongoDB with the user ID
            user_collection.update_one({"email_address":user['email_address']},{"$set":{"user_id":user['user_id']}})
        else:
            print("User ID already exists for email: {user['email_address']}")

        # Check if the user has a folder ID
        if user['folder_id'] in (None,''):
            # Create a folder for the user if they don't already have one
            folder_id = create_verified_folder(user['user_id'], headers)
            print('got folder id '+str(folder_id))
            if folder_id:
                print('updating folderid')
                print(folder_id)
                user['folder_id'] = folder_id
            #update the mongoDB with the folder ID
            print('updating mongodb')
            print(user['user_id'])
            print(user['folder_id'])
            user_collection.update_one({"user_id":user['user_id']},{"$set":{"folder_id":user['folder_id']}})

        else:
            print("Folder ID already exists for email: {user['email_address']}")
    return users    



if __name__ == "__main__":
    main()
