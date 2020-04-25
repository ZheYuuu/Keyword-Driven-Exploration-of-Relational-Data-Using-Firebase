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

### Server
#### Deploy docker container
- Fetch the docker image
`sudo docker pull zheyuuu/inf551`
- To add project configuration of firebase, need to create a file `.env`. The content of it like:
```
FLASK_APP=apps.py
FLASK_DEBUG=1
apiKey=[your own firebase apikey]
databaseURL=[your own firebase databseURL]
authDomain=[your own firebase authDomain]
storageBucket=[your own firebase storageBucket]
```
- Run docker container
```
sudo docker run -d --env-file=.env --name [container name] -p:[api server port you want to set]:5000 zheyuuu/inf551
```
#### API
Format: 

​	`[app uri]/[databse]/[table]`

​	eg. `localhost:5000/world/city`


