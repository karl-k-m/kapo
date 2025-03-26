# KaPo - Kaval Postkast
Kaval Postkast (KaPo) is a service for consuming and displaying messages sent between third parties. No relation to kaitsepolitsei.

# Deployment using Docker
KaPo is meant to be deployed as a docker container.

First, you probably want to change the db credentials to something slightly more secure in `docker-compose.yaml`.

To run, run following in project root:
`docker-compose up`  
This will create and start the Postgres and KaPo API containers.

# UI
A minimal UI is provided in this repository. Currently, KaPo does not provide a front-end deployment. So just open the index.html file in your client machine.  
If the backend runs on an external machine, you'll need to alter the URL-s in the script.js file to match that.
![image](https://github.com/user-attachments/assets/b45000cf-ff0f-47a4-8557-14650ad7eab3)
