# SecretStroll

## Introduction

In this project, you will develop a location-based application, SecretStroll,
that enables users to search for nearby points of interest (POI). We provide you
with a skeleton to help with the development.

**Virtualization.** We use Docker to enforce isolation between the client and
server on the virtual machine. Docker is a piece of software that uses the
capabilities of the Linux kernel to run processes in a sandboxed environment.
Thus, both the server and the client will "think" they are running in two
independent systems.

We also provide a virtual machine (VM) to facilitate the setup and configuration
of the SecretStroll and reduce potential networking problems while running the
application in different environments.

**Skeleton.** Both the client and the server provide a command-line interface to
run and interact with the server.  The underlying location-based service is
already implemented in the skeleton, and your task is to add the authentication
with attribute-based credentials.

We strongly recommend to use the `petrelic` cryptographic-pairing library to
implement PS credentials. You can find the project repository in
[https://github.com/spring-epfl/petrelic/](petrelic) and you can visit
[https://petrelic.readthedocs.io](docs) for documentation. This library is
bundled in the provided Docker container and virtual machines.

The skeleton has already implemented and integrated capabilities to save,
manage, and load keys and credentials as byte arrays. You need to implement
(de)serialization methods to match the API. We provide `serialization.py` as a
`petrelic` extension of `jsonpickle`, a serialization library, to help you with
the serialization of cryptographic objects.

Our skeleton and docker infrastructure takes care of syncing and deploying your
code. You only need to implement attribute-based credentials and update the
`stroll.py` file to use it.

**Testing**. An integral part of system development is testing the system. In
your implementation, you should check both success and failure paths when your
working with cryptographic primitives. In this project, you **must** use the
*pytest* framework to test your system. You can visit
[https://www.tutorialspoint.com/pytest/index.htm](pytest_turorials) for guides.


## Setting up the development environment

We use Python 3 in this project and all necessary Python components are already
installed on the VM and dockers. You can find installed libraries in the
`requirements.txt` file.

Feel free to have a look at `client.py` and `server.py` to see how the classes
and methods are used.

### Collaboration

You can use git repositories to sync your work with your teammates. However,
keep in mind that you are not allowed to use public repositories, so make sure
that your repository is **private**.

### Virtual machine

We provide you with a VM for SecretStroll project. We have already installed the
skeleton, and all the necessary applications and libraries on the VM. **We only
provide support for projects running inside the VM and we strongly recommend you
to develop inside the VM.**

There are two accounts on the VM (`user:password`):

```
student:student
root:root
```

You can set up ssh on the VM and connect from your host or directly use the VM
as your development environment.

### Setting up ssh in VirtualBox

In VirtualBox, you can set up ssh access to the VM by following these steps:

 * Open the settings of your image
 * Go to the "Network" panel
 * Choose "Advanced" and click on the "Port forwarding" button
 * Add a forwarding rule (green "plus" button on the side)
 * In the forwarding rule, leave IP addresses empty, set **Host port** to _2222_,
   and **Guest port** to 22 (the default SSH port)
 * Restart the virtual machine

Now, you can connect to your virtual machine via ssh:
`ssh -p 2222 student@127.0.0.1`

This is how you copy files _TO_ the VM:
`scp -P 2222 <path_to_copy_from_on_host_OS> student@127.0.0.1:<path_to_copy_to_on_guest_OS>`

Copy files _FROM_ the VM:
`scp -P 2222 student@127.0.0.1:<path_to_copy_from_on_guest_OS> <path_to_copy_to_on_host_OS> `


## Files in this repository

This repostory contains the skeleton code for Parts 1 and 3:

* `credential.py`—Source code that you have to complete.
* `stroll.py`—Source code that you have to complete.
* `client.py`—Client CLI calling classes and methods defined in `stroll.py`.
* `server.py`—Server CLI calling classes and methods defined in `stroll.py`.
* `serialization.py`—Extends the library `jsonpickle` to serialize python
  objects.
* `fingerprinting.py`—skeleton for Part 3.
* `requirements.txt`—Required Python libraries.
* `docker-compose.yaml`—*docker compose* configuration describing how to run the
  Docker containers.
* `docker/`—Directory containing Docker configurations for running the client
  and the server.
* `tor/`—Intentionally empty folder needed to run a Tor server.
* `fingerprint.db`—Database containing POI information for Part 3.

The directory `privacy_evaluation` contains files for the part 2.

## Server and client deployment

The server and client code deployment is handled by Docker and our skeleton. In
this section, we introduce our Docker infrastructure and how to use it. Then, we
provide a step-by-step guide of running the client and server.

### Working with the Docker infrastructure

*Before launching the infrastructure, ensure the `tor` directory in the project
skeleton has the correct permissions*
```
student@cs523:~/skeleton$ chmod 777 tor
student@cs523:~/skeleton$ ls -ld tor
drwxrwxrwx 2 student student    4096 mar 24 15:31 tor
```

The server and the client run in a Docker infrastructure composed of 2
containers, and a virtual network.

Before setting up the Docker infrastructure for the first time, you must first
build the images which will be used to run the client and server containers. To
do so, run the following command in the skeleton directory, which contains the
file `docker-compose.yml`:
```
docker-compose build
```

To set up the Docker infrastructure, run the following command in the directory
containing the file `docker-compose.yml`:
```
docker-compose up -d
```

When you stop working with the infrastructure, remember to shut it down by
running the following command in the directory containing the file
`docker-compose.yml`:
```
docker-compose down
```

*If you forget to shut down the Docker infrastructure, e.g., before shutting down
your computer, you might end up with stopped Docker containers preventing the
creation of the new ones when you to re-launch the infrastructure the next time.
This can be fixed by removing the network bridge with `docker-compose down` and
destroying the stopped Docker containers with `docker container prune -f`.*

### Accessing the data

The code of the skeleton is shared between your VM and Docker containers, so
modifications you make in your VM will also appear in containers. Feel free to
read the file `docker-compose.yml` to see how it is done.

If you need to transfer some data between your VM and your host machine, you can
set up ssh access and use the `scp` command as detailed before. Another option
is to have shared directories between the VM and your host. For this feature to
work correctly you have to install *Guest Additions* from VirtualBox on the VM
and refer to their documentation.



### Tor integration

If you use the skeleton, integrating Tor into your project should be seamless.
The Docker configuration we provide is designed to run Tor in the background,
and the code is designed to use the Tor if requested with no effort on your part.

If your project works if used normally, but fails when using Tor, you may
try to change the permission of the Tor directory with the following command
within the Docker container:

```
(server) $ chmod 700 /var/lib/tor/hidden_service/
```

If the problem persists, call an assistant.


### Server

It is easier to run the commands in a Docker container by opening a shell, and
then running the commands inside this shell.

To execute a shell in the container in which the server is to be launched, run
the following command:

```
docker exec -it cs523-server /bin/bash
```

In this container, the root directory of the project is mounted on `/server`.
```
cd /server
```

The server has two subcommands: `gen-ca` and `run`. `gen-ca` generates
the public and secret keys, and `run` runs the server. The server and its
subcommands have a help option, which you can access using the `-h` argument.

Key generation example:
```
python3 server.py setup -S restaurant -S bar -S sushi

usage: server.py setup [-h] [-p PUB] [-s SEC] -S SUBSCRIPTIONS

optional arguments:
  -h, --help            show this help message and exit
  -p PUB, --pub PUB     Name of the file in which to write the public key.
                        (default: key.pub)
  -s SEC, --sec SEC     Name of the file in which to write the secret key.
                        (default: key.sec)
  -S SUBSCRIPTIONS, --subscriptions SUBSCRIPTIONS
                        Subscriptions recognized by the server.
```

Server run example:
```
python3 server.py run

usage: server.py run [-h] [-p PUB] [-s SEC]

optional arguments:
  -h, --help         show this help message and exit
  -p PUB, --pub PUB  Name of the file containing the public key.
                     (default: key.pub)
  -s SEC, --sec SEC  Name of the file containing the secret key.
                     (default: key.sec)
```

In the Part 3 of the project, the server is expected to be accessible as a Tor
hidden service. The server's Docker container configures Tor to create a hidden
service and redirects the traffic to the Python server. The server serves local
and hidden service requests simultaneously by default.

The server also contains a database, `fingerprint.db`. This is used in Part 3.
The database has a POI table that contains records for each POI. The server
returns the list of POIs associated with a queried cell ID, and information
about each POI in the list. You must not modify the database.

### Client

To execute a shell in the client container, run the following command:

```
docker exec -it cs523-client /bin/bash
```

In this container, the root directory of the project is mounted on `/client`.
```
cd /client
```

The client has four subcommands: `get-pk`, `register`, `loc`, and `grid`. As for
the server, the client and its subcommands have a help option, which you can
access using the `-h` argument.

Use `get-pk` to retrieve the public key from the server:
```
python3 client.py get-pk

usage: client.py get-pk [-h] [-o OUT] [-t]

optional arguments:
  -h, --help         show this help message and exit
  -o OUT, --out OUT  Name of the file in which to write the public key.
                     (default: key-client.pub)
  -t, --tor          Use Tor to connect to the server.
```

Use `register` to register an account on the serve:
```
python3 client.py register -u your_name -S restaurant -S bar

usage: client.py register [-h] [-p PUB] -u USER [-o OUT] -S SUBSCRIPTIONS [-t]

optional arguments:
  -h, --help            show this help message and exit
  -p PUB, --pub PUB     Name of the file from which to read the public key.
                        (default: key-client.pub)
  -u USER, --user USER  User name.
  -o OUT, --out OUT     Name of the file in which to write the attribute-based
                        credential. (default: anon.cred)
  -S SUBSCRIPTIONS, --subscriptions SUBSCRIPTIONS
                        Subscriptions to register.
  -t, --tor             Use Tor to connect to the server.
```

Use `loc` and `grid` commands to retrieve information about points of interests
using lat/lon location (Part 1) and cell identifier (Part 3), respectively:
```
python3 client.py loc 46.52345 6.57890 -T restaurant -T bar

usage: client.py loc [-h] [-p PUB] [-c CREDENTIAL] -T TYPES [-t] lat lon

positional arguments:
  lat                   Latitude.
  lon                   Longitude.

optional arguments:
  -h, --help            show this help message and exit
  -p PUB, --pub PUB     Name of the file from which to read the public key.
                        (default: key-client.pub)
  -c CREDENTIAL, --credential CREDENTIAL
                        Name of the file from which to read the attribute-
                        based credential. (default: anon.cred)
  -T TYPES, --types TYPES
                        Types of services to request.
  -t, --tor             Use Tor to connect to the server.
```

**Warning**: The database only contains points of interest with latitude in
range \[46.5, 46.57\] and longitude in range \[6.55, 6.65\] (Lausanne area).
You can make queries outside these values, but you will not find anything
interesting.

```
python3 client.py grid 42 -T restaurant

usage: client.py grid [-h] [-p PUB] [-c CREDENTIAL] [-T TYPES] [-t] cell_id

positional arguments:
  cell_id               Cell identifier.

optional arguments:
  -h, --help            show this help message and exit
  -p PUB, --pub PUB     Name of the file from which to read the public key.
                        (default: key-client.pub)
  -c CREDENTIAL, --credential CREDENTIAL
                        Name of the file from which to read the attribute-
                        based credential. (default: anon.cred)
  -T TYPES, --types TYPES
                        Types of services to request.
  -t, --tor             Use Tor to connect to the server.
```

## A sample run of Part 1
Here we show a typical run of the system for Part 1.

Initialization:


Open a shell
```
$ cd skeleton
$ docker-compose build
$ docker-compose up -d
```

Server side:

Open a shell
```
$ cd skeleton
$ docker exec -it cs523-server /bin/bash
(server) $ cd /server
(server) $ python3 server.py setup -S restaurant -S bar -S dojo
(server) $ python3 server.py run -s key.sec -p key.pub
```

Client side:
```
Open a shell
$ cd skeleton
$ docker exec -it cs523-client /bin/bash
(client) $ cd /client
(client) $ python3 client.py get-pk
(client) $ python3 client.py register -u your_name -S restaurant -S bar -S dojo
(client) $ python3 client.py loc 46.52345 6.57890 -T restaurant -T bar
```

Close everything down at the end of the experiment:
```
$ docker-compose down
```

## A sample run of Part 3
Here we provide a typical run of the system for Part 3:

Initialization:

```
Open a shell
$ cd skeleton
$ docker-compose build
$ docker-compose up -d
```

Server side:

You should have already generated the keys in Part 1, so you do not need to
repeat that step.

```
Open a shell
$ cd skeleton
$ docker exec -it cs523-server /bin/bash
(server) $ cd /server
(server) $ python3 server.py run
```

Client side:

You should have already performed the registration in Part 1, so you do not need
to the repeat the step. Use the grid parameter to query for a particular cell.
Set the reveal argument (-r) to an empty value. Set the -t argument to use Tor. The example run below queries the server for cell ID = 42.

```
Open a shell
$ cd skeleton
$ docker exec -it cs523-client /bin/bash
(client) $ cd /client
(client) $ python3 client.py grid 42 -T restaurant -t
```

Close everything down at the end of the experiment:
```
$ docker-compose down
```
