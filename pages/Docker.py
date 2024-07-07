import streamlit as st
import docker

st.set_page_config(page_title="Docker")


services = ['Run Container', 'Start Container', 'Stop Container']
service = st.selectbox("Choose a Service", services)


client = docker.from_env()
if service == 'Run Container':
    image = st.text_input("Image name:tag")
    command = st.text_input("Command to run inside container")
    detach = st.selectbox("Detach mode",(True, False))
    container_config = {
        'image': image,  # Specify the Docker image to use
        'command': command,     # Specify the command to run inside the container
        'detach': detach             # Run the container in detached mode
    }

    pressed = st.button("Run")

    # Launch the container
    if pressed:
        container = client.containers.run(image, command, detach)
        # Print the container ID
        st.write("Container ID:", container)

elif service == 'Start Container':
    containers_list = client.containers.list(all=True)
    container = st.selectbox('Choose container', containers_list)

elif service == 'Start Container':
    containers_list = client.containers.list()
    container = st.selectbox('Choose container', containers_list)
