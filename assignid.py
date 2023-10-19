from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import VirtualMachine, VirtualMachineIdentity
from azure.mgmt.resource import ResourceManagementClient

# Define your Azure resource and VM specifics
subscription_id = '4a11049c-f1ef-4b33-8fdc-000845f3b37c'
resource_group_name = 'Marketplaceoffer'
vm_name = 'gtgapp'
identity_name = 'gtgidentity'

# Create Azure clients
credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)

# Get the identity's client ID
identity = resource_client.resources.get(resource_group_name, 'Microsoft.ManagedIdentity/userAssignedIdentities', identity_name)
identity_client_id = identity.properties['clientId']

# Get the existing VM
vm = compute_client.virtual_machines.get(resource_group_name, vm_name)

# Update the VM's identity to include the managed identity
vm.identity = VirtualMachineIdentity(
    type='UserAssigned',
    user_assigned_identities={identity_client_id: {}}
)

# Update the VM with the managed identity
compute_client.virtual_machines.begin_create_or_update(resource_group_name, vm_name, vm)
print(f"Managed identity '{identity_name}' assigned to Virtual Machine '{vm_name}'")
