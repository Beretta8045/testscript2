from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Azure Key Vault details
key_vault_name = 'gtgkeyvault2e'
secret_name = 'TenantID'

# Use an existing user-assigned identity
identity_client_id = 'gtgidentity'

# Read the Azure Tenant ID from the text file
tenant_id = None
with open('/path/to/your/config/file.txt', 'r') as config_file:
    for line in config_file:
        if line.startswith("Azure Tenant ID:"):
            tenant_id = line.split(":")[1].strip()
            break

if tenant_id is not None:
    # Authenticate using the existing user-assigned identity
    credential = DefaultAzureCredential(accepted_scopes=["https://vault.azure.net"])

    # Create a SecretClient object
    secret_client = SecretClient(vault_url=f"https://{key_vault_name}.vault.azure.net", credential=credential)

    # Create or update the secret in the Key Vault
    secret_bundle = secret_client.set_secret(secret_name, tenant_id)

    print(f"Azure Tenant ID '{tenant_id}' stored in Key Vault '{key_vault_name}' as secret '{secret_name}'")
else:
    print("Azure Tenant ID not found in the configuration file.")
