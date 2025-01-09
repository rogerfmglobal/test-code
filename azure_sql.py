"""
This module provides a class for counting Azure SQL Databases and aggregating their tags
in a specified Azure subscription using the Azure SDK for Python (azure-mgmt).
"""

from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient
from collections import defaultdict

class AzureSQLDBCounter:
    """
    A class to count Azure SQL Databases and aggregate their tags from a specified Azure subscription.

    Attributes:
        subscription_id (str): The Azure subscription ID to connect to.
        sql_client (SqlManagementClient): The Azure SqlManagementClient instance.
    """
    
    def __init__(self, subscription_id):
        self.subscription_id = subscription_id
        self.sql_client = SqlManagementClient(DefaultAzureCredential(), subscription_id)

    def get_count(self):
        """
        Retrieves the total number of Azure SQL Databases in the specified subscription.

        Returns:
            int: The total number of SQL Databases, or None if an error occurs.
        """
        try:
            sql_dbs = self.sql_client.databases.list()
            return sum(1 for _ in sql_dbs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_aggregated_tags(self):
        """
        Aggregates and retrieves tags for all Azure SQL Databases in the specified subscription.

        Returns:
            dict: A dictionary where keys are tag names and values are lists of tag values,
                  or None if an error occurs.
        """
        aggregated_tags = defaultdict(list)

        try:
            sql_dbs = self.sql_client.databases.list()
            for db in sql_dbs:
                if db.tags:
                    for key, value in db.tags.items():
                        aggregated_tags[key].append(value)
            return dict(aggregated_tags)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_status(self):
        """
        Returns the status of the Azure SQL Database service or None if it does not apply.
        
        Returns:
            str or None: The status of the SQL Database service if operational, else None.
        """
        try:
            sql_dbs = self.sql_client.databases.list()
            if any(True for _ in sql_dbs):
                return "Azure SQL Database Service is operational."
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage for AzureSQLDBCounter
if __name__ == "__main__":
    subscription_id = "<YOUR_AZURE_SUBSCRIPTION_ID>"  # Replace with your Azure Subscription ID
    azure_sql_db_counter = AzureSQLDBCounter(subscription_id)
    print(azure_sql_db_counter.get_sql_db_status())