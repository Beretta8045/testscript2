from azure.identity import DefaultAzureCredential  
from azure.mgmt.authorization import AuthorizationManagementClient  
from azure.mgmt.keyvault import KeyVaultManagementClient  
from azure.mgmt.resource import ResourceManagementClient  
from azure.mgmt.authorization.models import RoleDefinition  
  
# Set your Azure subscription ID  
subscription_id = "4a11049c-f1ef-4b33-8fdc-000845f3b37c"  
  
# Set your Azure resource group name and location  
resource_group_name = 'Marketplaceoffer'  
location = 'EastUS'  
  
# Set the name for the managed identity  
managed_identity_name = 'gtgidentity2'  
  
# Set the name for the Key Vault  
key_vault_name = 'gtgkeyvault'  
  
# Set the name for the Azure AD app  
aad_app_name = 'gtgapp4'  
  
# Initialize Azure credentials  
credentials = DefaultAzureCredential()  
  
# Initialize Azure clients  
resource_client = ResourceManagementClient(credentials, subscription_id)  
authorization_client = AuthorizationManagementClient(credentials, subscription_id)  
keyvault_client = KeyVaultManagementClient(credentials, subscription_id)  
  
# Create the managed identity  
identity_params = {  
    'location': location,  
    'identity': {  
        'type': 'SystemAssigned'  
    }  
}  
identity = resource_client.managed_identities.create_or_update(resource_group_name, managed_identity_name, identity_params).result()  
  
# Assign permissions to Key Vault  
keyvault_client.role_assignments.create(  
scope = "/subscriptions/{}/resourceGroups/{}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{}".format(subscription_id, resource_group_name, managed_identity_name)  
keyvault_client.role_assignments.create(  
    scope=scope,  
    role_definition_name="8e3af657-a8ff-443c-a75c-2fe8c4bcb635",  
    principal_id=identity.principal_id  
)  
  
# Register Azure AD app  
app = authorization_client.create_application(resource_group_name, aad_app_name)  
  
print(f"Managed identity created with name: {identity.name}")  
print(f"Managed identity principal ID: {identity.principal_id}")  
print(f"Key Vault permissions assigned to the managed identity")  
print(f"Azure AD app registered with name: {app.display_name}")  
