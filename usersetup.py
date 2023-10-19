import tkinter as tk
from tkinter import Label, Entry, Button

def save_variables():
    tenant_id = tenant_id_entry.get()
    subscription_id = subscription_id_entry.get()
    license_key = license_key_entry.get()

    with open("/usr/local/bin/setup.txt", "w") as config_file:
        config_file.write(f"Azure Tenant ID: {tenant_id}\n")
        config_file.write(f"Azure Subscription ID: {subscription_id}\n")
        config_file.write(f"License Key: {license_key}\n")

    root.destroy()

root = tk.Tk()
root.title("Azure Configuration")

tenant_id_label = Label(root, text="Azure Tenant ID:")
tenant_id_label.pack()
tenant_id_entry = Entry(root)
tenant_id_entry.pack()

subscription_id_label = Label(root, text="Azure Subscription ID:")
subscription_id_label.pack()
subscription_id_entry = Entry(root)
subscription_id_entry.pack()

license_key_label = Label(root, text="License Key:")
license_key_label.pack()
license_key_entry = Entry(root)
license_key_entry.pack()

save_button = Button(root, text="Save", command=save_variables)
save_button.pack()

root.mainloop()
