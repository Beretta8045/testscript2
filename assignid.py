from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import VirtualMachine, VirtualMachineIdentity
from azure.mgmt.resource import ResourceManagementClient

# Define your Azure resource and VM specifics
subscription_id = 'YOUR_SUBSCRIPTION_ID'
resource_group_name = 'YOUR_RESOURCE_GROUP'
vm_name = 'YOUR_VM_NAME'
identity_name = 'YOUR_MANAGED_IDENTITY_NAME'

# Create Azure clients
credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)

# Create or update the user-defined identity
resource_client.resources.begin_create_or_update(
    resource_group_name,
    'Microsoft.ManagedIdentity/userAssignedIdentities',
    identity_name,
    {
        'location': 'eastus'  # Update with your desired location
    }
).result()

# Get the identity's client ID
identity = resource_client.resources.get(resource_group_name, 'Microsoft.ManagedIdentity/userAssignedIdentities', identity_name)
identity_client_id = identity.properties['clientId']

# Create a Virtual Machine with the assigned managed identity
vm = VirtualMachine(
    location='eastus',  # Update with your desired location
    identity=VirtualMachineIdentity(type='UserAssigned', user_assigned_identities={identity_client_id: {}}),
    os_profile={
        'computer_name': vm_name,
        'admin_username': 'youradminuser',  # Update with your desired admin username
        'admin_password': 'youradminpassword'  # Update with your desired admin password
    },
    hardware_profile={
        'vm_size': 'Standard_DS2_v2'  # Update with your desired VM size
    }
)

compute_client.virtual_machines.create_or_update(resource_group_name, vm_name, vm)
print(f"Virtual Machine '{vm_name}' created with managed identity '{identity_name}'")
