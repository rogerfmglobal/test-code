"""
This module provides a class for counting Azure Virtual Machines (VMs) and aggregating their tags
in a specified Azure subscription using the Azure SDK for Python (azure-mgmt).
"""

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from collections import defaultdict

class AzureVMCounter:
    """
    A class to count Azure Virtual Machines and aggregate their tags from a specified Azure subscription.

    Attributes:
        subscription_id (str): The Azure subscription ID to connect to.
        compute_client (ComputeManagementClient): The Azure ComputeManagementClient instance.
    """
    
    def __init__(self, subscription_id):
        self.subscription_id = subscription_id
        self.compute_client = ComputeManagementClient(DefaultAzureCredential(), subscription_id)

    def get_vm_count(self):
        """
        Retrieves the total number of Azure Virtual Machines in the specified subscription.

        Returns:
            int: The total number of VMs, or None if an error occurs.
        """
        try:
            vms = self.compute_client.virtual_machines.list_all()
            return sum(1 for _ in vms)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_aggregated_vm_tags(self):
        """
        Aggregates and retrieves tags for all Azure VMs in the specified subscription.

        Returns:
            dict: A dictionary where keys are tag names and values are lists of tag values,
                  or None if an error occurs.
        """
        aggregated_tags = defaultdict(list)

        try:
            vms = self.compute_client.virtual_machines.list_all()
            for vm in vms:
                if vm.tags:
                    for key, value in vm.tags.items():
                        aggregated_tags[key].append(value)
            return dict(aggregated_tags)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_vm_status(self):
        """
        Returns the status of the Azure VM service or None if it does not apply.
        
        Returns:
            str or None: The status of the VM service if operational, else None.
        """
        try:
            vms = self.compute_client.virtual_machines.list_all()
            if any(True for _ in vms):
                return "Azure VM Service is operational."
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage for AzureVMCounter
if __name__ == "__main__":
    subscription_id = "<YOUR_AZURE_SUBSCRIPTION_ID>"  # Replace with your Azure Subscription ID
    azure_vm_counter = AzureVMCounter(subscription_id)
    print(azure_vm_counter.get_vm_status())