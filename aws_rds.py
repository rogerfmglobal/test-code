"""
This module provides a class for counting RDS instances and aggregating their tags
in a specified AWS region using the Boto3 library.

The RDSInstanceCounter class allows users to interact with AWS RDS instances
to retrieve the total number of RDS instances and the tags associated with those
instances in an easy-to-use manner.

Usage example:
    counter = RDSInstanceCounter(region_name='us-west-2')
    rds_instance_count = counter.get_rds_instance_count()
    aggregated_tags = counter.get_aggregated_rds_tags()
"""

import boto3
from collections import defaultdict

class RDSInstanceCounter:
    """
    A class to count RDS instances and aggregate their tags from a specified AWS region.

    Attributes:
        region_name (str): The AWS region to connect to. Default is 'us-east-1'.
        rds_client (boto3.client): The Boto3 RDS client instance.
    """
    
    def __init__(self, region_name='us-east-1'):
        """
        Initializes the RDSInstanceCounter with the specified region.

        Args:
            region_name (str): The AWS region to initialize the RDS client (default is 'us-east-1').
        """
        self.rds_client = boto3.client('rds', region_name=region_name)

    def get_rds_instance_count(self):
        """
        Retrieves the total number of RDS instances in the specified region.

        Returns:
            int: The total number of RDS instances, or None if an error occurs.
        """
        try:
            response = self.rds_client.describe_db_instances()
            rds_instance_count = len(response['DBInstances'])
            return rds_instance_count
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_aggregated_rds_tags(self):
        """
        Aggregates and retrieves tags for all RDS instances in the specified region.

        Returns:
            dict: A dictionary where keys are tag names and values are lists of tag values,
                  or None if an error occurs.
        """
        aggregated_tags = defaultdict(list)

        try:
            response = self.rds_client.describe_db_instances()

            # Iterate through RDS instances
            for instance in response['DBInstances']:
                # Retrieve tags for each RDS instance
                tags_response = self.rds_client.list_tags_for_resource(
                    ResourceName=instance['DBInstanceArn']
                )
                # Check if the instance has tags
                if 'TagList' in tags_response:
                    for tag in tags_response['TagList']:
                        aggregated_tags[tag['Key']].append(tag['Value'])

            return dict(aggregated_tags)  # Convert defaultdict to a regular dict for the output

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_rds_status(self):
        """
        Returns the status of the RDS service or None if it does not apply.

        Returns:
            str or None: The status of the RDS service if operational, else None.
        """
        try:
            response = self.rds_client.describe_orderable_db_instance_options()
            if response['OrderableDBInstanceOptions']:
                return "RDS Service is operational."
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
if __name__ == "__main__":
    counter = RDSInstanceCounter()
    count = counter.get_rds_instance_count()
    if count is not None:
        print(f"Total RDS Instances: {count}")
    
    tags = counter.get_aggregated_rds_tags()
    if tags is not None:
        for key, values in tags.items():
            print(f"{key}: {', '.join(values)}")

    status = counter.get_rds_status()
    if status is not None:
        print(status)
