"""
This module provides a class for counting Azure Network Security Groups (NSGs) and aggregating their tags
in a specified Azure subscription using the Azure SDK for Python (azure-mgmt).
"""

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from collections import defaultdict

class AzureNSGCounter:
    """
    A class to count Azure Network Security Groups (NSGs) and aggregate their tags from a specified Azure subscription.

    Attributes:
        subscription_id (str): The Azure subscription ID to connect to.
        network_client (NetworkManagementClient): The Azure NetworkManagementClient instance.
    """
    
    def __init__(self, subscription_id):
        self.subscription_id = subscription_id
        self.network_client = NetworkManagementClient(DefaultAzureCredential(), subscription_id)

    def get_nsg_count(self):
        """
        Retrieves the total number of Azure Network Security Groups in the specified subscription.

        Returns:
            int: The total number of NSGs, or None if an error occurs.
        """
        try:
            return sum(1 for _ in self.network_client.network_security_groups.list_all())
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_aggregated_nsg_tags(self):
        """
        Aggregates and retrieves tags for all Azure NSGs in the specified subscription.

        Returns:
            dict: A dictionary where keys are tag names and values are lists of tag values,
                  or None if an error occurs.
        """
        aggregated_tags = defaultdict(list)

        try:
            nsgs = self.network_client.network_security_groups.list_all()
            for nsg in nsgs:
                if nsg.tags:
                    for key, value in nsg.tags.items():
                        aggregated_tags[key].append(value)
            return dict(aggregated_tags)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_nsg_status(self):
        """
        Returns the status of the Azure NSG service or None if it does not apply.
        
        Returns:
            str or None: The status of the NSG service if operational, else None.
        """
        try:
            nsgs = self.network_client.network_security_groups.list_all()
            if any(True for _ in nsgs):
                return "Azure NSG Service is operational."
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage for AzureNSGCounter
if __name__ == "__main__":
    subscription_id = "<YOUR_AZURE_SUBSCRIPTION_ID>"  # Replace with your Azure Subscription ID
    azure_nsg_counter = AzureNSGCounter(subscription_id)
    print(azure_nsg_counter.get_nsg_status())