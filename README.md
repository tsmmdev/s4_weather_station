# TODO #
### - Readme ###
### - deploy.sh for client and server ###


The error you're encountering suggests that a certificate file (certfile) must be specified for server-side SSL/TLS operations, even if you're not requiring client certificates. This requirement is a default behavior in many SSL/TLS implementations and libraries, including Python's ssl module.

While SSL/TLS connections can technically be established without certificates, the use of certificates is strongly recommended for security reasons. However, if you still want to proceed without certificates, you might need to create a dummy certificate for the server to use. This dummy certificate can be self-signed and doesn't need to be issued by a trusted certificate authority.

Here's a basic example of how you can generate a self-signed certificate using OpenSSL:

bash

openssl req -x509 -newkey rsa:4096 -keyout server_key.pem -out server_cert.pem -days 365 -nodes

This command generates a self-signed certificate (server_cert.pem) along with its private key (server_key.pem). You can then specify these files in your server code when creating the SSL context.

Keep in mind that while using self-signed certificates may allow your server to run without encountering the specific error you're seeing, it's crucial to understand the security implications and risks associated with self-signed certificates, especially in production environments. Always consider using properly issued certificates from a trusted certificate authority for secure communication.




# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact