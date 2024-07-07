import streamlit as st
import boto3
import os
import tempfile

st.set_page_config(page_title="AWS Services")

services=['Launch Instance','Start Instances','Stop Instances', 'Terminate Instances', 'S3 Upload', 'S3 Delete']
instancesList = []


# list of stopped instances
def list_stopped_ec2_instances():
    # Create a boto3 EC2 client
    ec2_client = boto3.client('ec2')
    
    # Call describe_instances to get the details of all instances
    response = ec2_client.describe_instances()
    
    stopped_instance_ids = []
    
    # Iterate through the reservations and instances to get instance details
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == 'stopped':
                stopped_instance_ids.append(instance['InstanceId'])
    
    return stopped_instance_ids


# list of running instances
def list_running_ec2_instances():
    # Create a boto3 EC2 client
    ec2_client = boto3.client('ec2')
    
    # Call describe_instances to get the details of all instances
    response = ec2_client.describe_instances()
    
    running_instance_ids = []
    
    # Iterate through the reservations and instances to get instance details
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == 'running':
                running_instance_ids.append(instance['InstanceId'])
    
    return running_instance_ids

# get list of all instances
def list_all_ec2_instances():
    # Create a boto3 EC2 client
    ec2_client = boto3.client('ec2')
    
    # Call describe_instances to get the details of all instances
    response = ec2_client.describe_instances()
    
    all_instance_ids = []
    
    # Iterate through the reservations and instances to get instance details
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            all_instance_ids.append(instance['InstanceId'])
    
    return all_instance_ids



def list_s3_buckets():
    # Create an S3 client
    s3 = boto3.client('s3')
    try:
        # Get a list of all S3 buckets
        response = s3.list_buckets()

        # Extract bucket names from the response
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]

        return bucket_names
    except Exception as e:
        return f"Error listing S3 buckets: {e}"


def upload_to_s3(file_path, bucket_name, object_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file to the specified bucket
        s3.upload_file(file_path, bucket_name, object_name)
        return f"File uploaded successfully to s3://{bucket_name}/{object_name}"
    except Exception as e:
        return f"Error uploading file: {e}"

# Replace these values with your own
file_path = 'path/to/your/file.txt'
bucket_name = 'your-bucket-name'
object_name = 'file.txt'

# Call the function to upload the file
# upload_to_s3(file_path, bucket_name, object_name)

# print(list_s3_buckets())


service = st.selectbox(
    'Choose any Service',
     services)

if 'start_instances' not in st.session_state:
    st.session_state.start_instances = []


# Launch Instances
if service == 'Launch Instance':
    numbers = st.selectbox(
        'Enter the number of Instances',
        [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    
    launch = st.button('Launch')

# Start Instances
elif service == 'Start Instances':
    to_start_list = []
    start_instances_list = list_stopped_ec2_instances()
    for instance in start_instances_list:
        check = st.checkbox(instance)
        if check:
            to_start_list.append(instance)
    
    # start_instances_list

    start = st.button('Start')
    ec2_client = boto3.client('ec2')
    if start:
        try:
            response = ec2_client.start_instances(InstanceIds=to_start_list)
            st.write('Instances Started Successfully')
        except Exception as e:
            print(f'Error Starting Instance: {e}')
    
    # st.session_state.start_instances.append(start_instances_list)
    # st.session_state

# Stop Instances
elif service == 'Stop Instances':
    to_stop_list = []
    stop_instances_list = list_running_ec2_instances()
    for instance in stop_instances_list:
        check = st.checkbox(instance)
        if check:
            to_stop_list.append(instance)
    
    # stop_instances_list

    stop = st.button('Stop')
    ec2_client = boto3.client('ec2')
    if stop:
        try:
            response = ec2_client.stop_instances(InstanceIds=to_stop_list)
            st.write('Instances Stopped Successfully')
        except Exception as e:
            print(f'Error Stopped Instance: {e}')

# Terminate Instances
elif service == 'Terminate Instances':
    to_terminate_list = []
    terminate_instances_list = list_all_ec2_instances()
    for instance in terminate_instances_list:
        check = st.checkbox(instance)
        if check:
            to_terminate_list.append(instance)
    
    # terminate_instances_list

    terminate = st.button('Terminate')
    ec2_client = boto3.client('ec2')
    if terminate:
        try:
            response = ec2_client.terminate_instances(InstanceIds=to_terminate_list)
            st.write('Instances terminated Successfully')
        except Exception as e:
            print(f'Error Terminating Instance: {e}')


# Upload file to S3 Bucket
elif service == 'S3 Upload':
    bucket_list = list_s3_buckets()
    check = st.radio("Choose a Bucket", bucket_list)
    file = st.file_uploader("Upload a file")
    object = st.text_input("Enter the object name")
    pressed = st.button("Upload")
    if pressed:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file.read())
        file_path = temp_file.name
        temp_file.close()

        feedback = upload_to_s3(file_path, check, object)
        st.write(feedback)

elif service == 'S3 Delete':
    bucket_list = list_s3_buckets()
    check = st.radio("Choose a Bucket", bucket_list)
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=check)

    # Check if objects are present in the bucket
    if 'Contents' in response:
        # Extract file names from the response
        file_list = [obj['Key'] for obj in response['Contents']]
        
        # Print the list of file names
        selected_file = st.radio("Choose a file:", file_list)
        pressed = st.button("Delete")
        if pressed:
            try:
                response = s3.delete_object(Bucket=check, Key=selected_file)
                st.write(f'File {selected_file} deleted successfully.')
            except Exception as e:
                print(f'Error deleting file: {e}')

    else:
        st.write('No objects found in the bucket.')


