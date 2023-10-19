from azure.identity import DefaultAzureCredential  
from azure.keyvault.secrets import SecretClient  
from jwt import decode

# Set your Azure subscription ID, resource group name, Key Vault name, and secret name  
subscription_id = '4a11049c-f1ef-4b33-8fdc-000845f3b37c'  
resource_group_name = 'Marketplaceoffer'  
key_vault_name = 'gtgkeyvault2'  
secret_name = 'TENANT_ID_SECRET_NAME'  

# Create a DefaultAzureCredential object  
credential = DefaultAzureCredential()  

# Retrieve the Azure Tenant ID
token = credential.get_token("https://management.azure.com/.default")
access_token = token.token
decoded_token = decode(access_token, verify=False)
tenant_id = decoded_token['tid']

# Create a SecretClient object  
secret_client = SecretClient(vault_url=f"https://{key_vault_name}.vault.azure.net", credential=credential)  

# Store the Tenant ID in the Key Vault as a secret  
secret_client.set_secret(secret_name, tenant_id)  

print(f"Azure Tenant ID '{tenant_id}' stored in Key Vault '{key_vault_name}' as secret '{secret_name}'")
