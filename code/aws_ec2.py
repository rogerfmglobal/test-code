"""
This module provides a class for counting EC2 instances and aggregating their tags
in a specified AWS region using the Boto3 library.

The EC2InstanceCounter class allows users to interact with AWS EC2 resources
to retrieve the total number of instances and the tags associated with those
instances in an easy-to-use manner.

Usage example:
    counter = EC2InstanceCounter(region_name='us-west-2')
    instance_count = counter.get_instance_count()
    aggregated_tags = counter.get_aggregated_ec2_tags()
"""

import boto3
from collections import defaultdict

class EC2InstanceCounter:
    """
    A class to count EC2 instances and aggregate their tags from a specified AWS region.

    Attributes:
        region_name (str): The AWS region to connect to. Default is 'us-east-1'.
        ec2_client (boto3.client): The Boto3 EC2 client instance.
    """
    
    def __init__(self, region_name='us-east-1'):
        """
        Initializes the EC2InstanceCounter with the specified region.

        Args:
            region_name (str): The AWS region to initialize the EC2 client (default is 'us-east-1').
        """
        self.ec2_client = boto3.client('ec2', region_name=region_name)

    def get_count(self):
        """
        Retrieves the total number of EC2 instances in the specified region.

        Returns:
            int: The total number of EC2 instances, or None if an error occurs.
        """
        try:
            response = self.ec2_client.describe_instances()
            instance_count = sum(
                len(reservation['Instances']) for reservation in response['Reservations']
            )
            return instance_count
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_aggregated_tags(self):
        """
        Aggregates and retrieves tags for all EC2 instances in the specified region.

        Returns:
            dict: A dictionary where keys are tag names and values are lists of tag values,
                  or None if an error occurs.
        """
        aggregated_tags = defaultdict(list)

        try:
            # Retrieve all EC2 instances
            response = self.ec2_client.describe_instances()

            # Iterate through reservations and instances
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    # Check if the instance has tags
                    if 'Tags' in instance:
                        for tag in instance['Tags']:
                            # Aggregate tags by key
                            aggregated_tags[tag['Key']].append(tag['Value'])

            return dict(aggregated_tags)  # Convert defaultdict to a regular dict for the output

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_status(self):
        """
        Returns the status of the EC2 service or None if it does not apply.
        
        Returns:
            str or None: The status of the EC2 service if operational, else None.
        """
        try:
            response = self.ec2_client.describe_account_attributes(AttributeNames=['maxInstances'])
            if response['AccountAttributes']:
                return "EC2 Service is operational."
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
if __name__ == "__main__":
    counter = EC2InstanceCounter()
    count = counter.get_instance_count()
    if count is not None:
        print(f"Total EC2 Instances: {count}")
    
    tags = counter.get_aggregated_ec2_tags()
    if tags is not None:
        for key, values in tags.items():
            print(f"{key}: {', '.join(values)}")

    status = counter.get_ec2_status()
    if status is not None:
        print(status)
