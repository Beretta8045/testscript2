from azure.identity import DefaultAzureCredential  
from azure.keyvault.secrets import SecretClient  
  
# Set your Azure subscription ID, resource group name, Key Vault name, and secret name  
subscription_id = '4a11049c-f1ef-4b33-8fdc-000845f3b37c'  
resource_group_name = 'Marketplaceoffer'  
key_vault_name = 'gtgkeyvault2'  
secret_name = 'TENANT_ID_SECRET_NAME'  
  
from azure.identity import ManagedIdentityCredential  
from azure.keyvault.secrets import SecretClient  
  
# Set your Azure resource group name, Key Vault name, and secret name  
resource_group_name = 'your_resource_group_name'  
key_vault_name = 'your_key_vault_name'  
secret_name = 'your_secret_name'  
  
# Create a ManagedIdentityCredential object  
credential = ManagedIdentityCredential()  
  
# Retrieve the Azure Tenant ID using the ManagedIdentityCredential  
tenant_id = credential.get_token("https://management.azure.com/.default").tenant_id  
  
# Create a SecretClient object  
secret_client = SecretClient(vault_url=f"https://{key_vault_name}.vault.azure.net", credential=credential)  
  
# Store the Tenant ID in the Key Vault as a secret  
secret_client.set_secret(secret_name, tenant_id)  
  
print(f"Azure Tenant ID '{tenant_id}' stored in Key Vault '{key_vault_name}' as secret '{secret_name}'")  
