"""
This module provides a class for counting EC2 security groups and aggregating their tags
in a specified AWS region using the Boto3 library.

The EC2SecurityGroupCounter class allows users to interact with AWS EC2 security groups
to retrieve the total number of security groups and the tags associated with those
security groups in an easy-to-use manner.

Usage example:
    counter = EC2SecurityGroupCounter(region_name='us-west-2')
    security_group_count = counter.get_security_group_count()
    aggregated_tags = counter.get_aggregated_sg_tags()
"""

import boto3
from collections import defaultdict

class EC2SecurityGroupCounter:
    """
    A class to count EC2 security groups and aggregate their tags from a specified AWS region.

    Attributes:
        region_name (str): The AWS region to connect to. Default is 'us-east-1'.
        ec2_client (boto3.client): The Boto3 EC2 client instance.
    """
    
    def __init__(self, region_name='us-east-1'):
        """
        Initializes the EC2SecurityGroupCounter with the specified region.

        Args:
            region_name (str): The AWS region to initialize the EC2 client (default is 'us-east-1').
        """
        self.ec2_client = boto3.client('ec2', region_name=region_name)

    def get_security_group_count(self):
        """
        Retrieves the total number of security groups in the specified region.

        Returns:
            int: The total number of security groups, or None if an error occurs.
        """
        try:
            response = self.ec2_client.describe_security_groups()
            security_group_count = len(response['SecurityGroups'])
            return security_group_count
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_aggregated_sg_tags(self):
        """
        Aggregates and retrieves tags for all EC2 security groups in the specified region.

        Returns:
            dict: A dictionary where keys are tag names and values are lists of tag values,
                  or None if an error occurs.
        """
        aggregated_tags = defaultdict(list)

        try:
            response = self.ec2_client.describe_security_groups()

            # Iterate through security groups
            for security_group in response['SecurityGroups']:
                # Check if the security group has tags
                if 'Tags' in security_group:
                    for tag in security_group['Tags']:
                        # Aggregate tags by key
                        aggregated_tags[tag['Key']].append(tag['Value'])

            return dict(aggregated_tags)  # Convert defaultdict to a regular dict for the output

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_sg_status(self):
        """
        Returns the status of the Security Groups service or None if it does not apply.
        
        Returns:
            str or None: The status of the Security Groups service if operational, else None.
        """
        try:
            response = self.ec2_client.describe_security_groups()
            if response['SecurityGroups']:
                return "Security Groups Service is operational."
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
if __name__ == "__main__":
    counter = EC2SecurityGroupCounter()
    count = counter.get_security_group_count()
    if count is not None:
        print(f"Total Security Groups: {count}")
    
    tags = counter.get_aggregated_sg_tags()
    if tags is not None:
        for key, values in tags.items():
            print(f"{key}: {', '.join(values)}")

    status = counter.get_sg_status()
    if status is not None:
        print(status)
