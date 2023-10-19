from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


# Define the Key Vault URL and the name for the secret that will store the tenant ID
TENANT_ID_SECRET_NAME = "azure-ad-tenant-id"
VAULT_URL = os.environ["https://gtgkeyvault1.vault.azure.net"]
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://gtgkeyvault1.vault.azure.net", credential=credential)
secret = secret_client.set_secret("secret-name", "secret-value")

# Use Managed Identity to authenticate to Azure Key Vault
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

# Capture the Azure AD Tenant ID for the current subscription
try:
    tenant_id = os.environ["AZURE_TENANT_ID"]
    print("Captured Azure AD Tenant ID: %s" % tenant_id)

    # Store the Tenant ID in the Key Vault as a secret
    secret_client.set_secret(TENANT_ID_SECRET_NAME, tenant_id)
    print("Tenant ID stored in Key Vault as secret: {}".format(TENANT_ID_SECRET_NAME))
except KeyError:
    print("Azure AD Tenant ID is not available in the environment variables.")

# Capture the Azure AD Tenant Name for the current subscription
try:
    tenant_name = os.environ["AZURE_AD_TENANT_NAME"]
    print("Captured Azure AD Tenant Name: %s" % tenant_name)

    # Store the Tenant Name in the Key Vault as a secret
    secret_name = "azure-ad-tenant-name"  # Name for the secret
    secret_client.set_secret(secret_name, tenant_name)
    print(f"Tenant Name stored in Key Vault as secret: {secret_name}")
except KeyError:
    print("Azure AD Tenant Name is not available in the environment variables.")
