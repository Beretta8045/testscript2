import argparse

parser = argparse.ArgumentParser(description="Azure Configuration Setup")
parser.add_argument("--tenant_id", type=str, help="Azure Tenant ID")
parser.add_argument("--subscription_id", type=str, help="Azure Subscription ID")
parser.add_argument("--license_key", type=str, help="License Key")

args = parser.parse_args()

if args.tenant_id and args.subscription_id and args.license_key:
    with open("/path/to/your/config/file.txt", "w") as config_file:
        config_file.write(f"Azure Tenant ID: {args.tenant_id}\n")
        config_file.write(f"Azure Subscription ID: {args.subscription_id}\n")
        config_file.write(f"License Key: {args.license_key}\n")
else:
    print("Please provide Azure Tenant ID, Azure Subscription ID, and License Key as command-line arguments.")
