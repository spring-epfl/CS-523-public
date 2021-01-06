# Secure Multi-party Computation System

## Introduction

In this project, you will develop a secure multi-party computation system in
Python 3. We provide you this code skeleton to help with the development.

We also provide a virtual machine (VM) to facilitate the setup and configuration
of the system and reduce potential networking problems which might happen while
running the application in different environments.

### Skeleton
You will have to implement the SMC client, the trusted parameter generator,
secret sharing mechanisms, and tools for specifying expressions to compute. We
already implemented network communications and the trusted server, along with a
test suite that your implementation will have to pass.

#### Files in the skeleton

The skeleton contains the following files.

Components for building an SMC protocol. You should modify these:
* `expression.py`—Tools for defining arithmetic expressions.
* `secret_sharing.py`—Secret sharing scheme
* `ttp.py`—Trusted parameter generator for the Beaver multiplication scheme.
* `smc_party.py`—SMC party implementation
* `test_integration.py`—Integration test suite.
* `test_expression.py`—Template of a test suite for expression handling.
* `test_ttp.py`—Template of a test suite for the trusted parameter generator.
* `test_secret_sharing.py`—Template of a test suite for secret sharing.

Code that handles the communication. You should not need to modify these files unless
you bump into some serialization issues.
* `protocol.py`—Specification of SMC protocol
* `communication.py`—SMC party-side of communication
* `server.py`—Trusted server to exchange information between SMC parties

Read the comments in each of the files for more details and pointers.

#### Requirements and what files should you change
As you can see above, you can change most of the files in this skeleton.
However, the **requirement** is that all existing tests in `test_integration.py`
should pass **without any modification** (you can, however, add new tests.) We
will test your solution using our own version of ``test_integration.py`` and all
failing tests will negatively contribute to the grade.

### Testing

An integral part of a system development is testing.
For this first project, we provide you with an integration test suite to ensure
the functionalities you will have to implement works correctly.

They are implemented using *pytest*, and you can run them using the command
```
python3 -m pytest
```
in the directory of the skeleton.

If you want to run only one specific test suite, you can specify the file in
the command line. For example, if we only want to test our implementation for
handling the expression, we will run the following command:
```
python3 -m pytest test_expression.py
```
In some versions, pytest captures the program output, and only displays the
result of the test. When debugging, you can disable this capture by passing the
option `-s` to Pytest.
```
python3 -m pytest -s
```

When running the integration test suite, you will notice that it will run SMC
parties and trusted server as independent processes and that these processes
will communicate via a network.

You are free to write additional test suites to ensure your code is working as
you expect. Consult the description of the files in the project for some
skeleton test files.

## Setting up the development environment

We provide you a VM for this project with all necessary Python dependencies
already installed.

If you are using the provided VM you can skip this section.

If you are not using the VM, you will need to install Python 3 on your machine.
This code was implemented and tested with Python 3.6, you may want to install a
higher version, in which case, ensure that you only use features supported by
Python 3.6 in your code.

You can install the dependant python libraries by running the command
```
python3 -m pip install -r requirements.txt
```
in the directory of the skeleton.

Also, the name given to the Python binary might differ depending on your
system, in the VM we provided, the command which refers specifically to the
Python 3 interpreter is `python3`, in some systems, the command might simply be
called `python`. So when running the commands we provide, ensure you are using
the correct interpreter.

**Note:** For your curiosity, the network communications rely on the library *Requests*,
and on the *Flask* framework, while the tests are implemented with the *pytest*
framework.
Feel free to check their documentation, if you would like to understand in
details how they work, and feel free to have a look at the files
`communication.py`, `server.py`, and at the test suites to see how we use these
library and frameworks in practice.

### Collaboration

You can use git repositories to sync your work with your teammates. However,
keep in mind that you are not allowed to use public repositories, so make sure
that your repository is **private**.

### Virtual machine

We provide you with a VM for the secure multi-party computation system.
We have already installed the skeleton, and all the necessary applications and
libraries on the VM.
**We only provide support for projects running inside the VM and we strongly
recommend you to develop inside the VM.**

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
```
ssh -p 2222 student@127.0.0.1
```

This is how you copy files _TO_ the VM:
```
scp -P 2222 <path_to_copy_from_on_host_OS> student@127.0.0.1:<path_to_copy_to_on_guest_OS>
```

Copy files _FROM_ the VM:
```
scp -P 2222 student@127.0.0.1:<path_to_copy_from_on_guest_OS> <path_to_copy_to_on_host_OS>
```

Another option to exchange data is to have shared directories between the VM
and your host.
For this feature to work correctly you have to install *Guest Additions* from
VirtualBox on the VM and refer to their documentation.


## Example of a test run

Once a part of your project is finished, you can test if it works correctly with
*pytest*.  Here is an example of output that the tests might produce if your
project is well implemented.

```
python3 -m pytest -s
============================= test session starts =============================
platform linux -- Python 3.6.9, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: /home/student/Desktop/solution
plugins: cov-2.11.1
collected 25 items

test_expression.py .
test_integration.py [ PUBLISH  ] SENDER Alice / LABEL final
Alice has finished!
Server stopped.
.[ PUBLISH  ] SENDER Alice / LABEL final
Alice has finished!
Server stopped.
.[ SEND     ] SENDER Alice / LABEL 4f3963326a673d3d / RECEIVER Bob
[ SEND     ] SENDER Bob / LABEL 434e38516c413d3d / RECEIVER Alice
[ SEND     ] SENDER Alice / LABEL 3067437662413d3d / RECEIVER Bob
[ RETRIEVE ] RECEIVER Bob / LABEL 4f3963326a673d3d
[ RETRIEVE ] RECEIVER Alice / LABEL 434e38516c413d3d
[ RETRIEVE ] RECEIVER Bob / LABEL 3067437662413d3d
[ PUBLISH  ] SENDER Alice / LABEL final
[ PUBLISH  ] SENDER Bob / LABEL final
[ RETRIEVE ] RECEIVER Alice. LABEL final / SENDER Bob
[ RETRIEVE ] RECEIVER Bob. LABEL final / SENDER Alice
Alice has finished!
Bob has finished!
Server stopped.
.[ SEND     ] SENDER Alice / LABEL 3562684370413d3d / RECEIVER Bob
[ SEND     ] SENDER Bob / LABEL 4d6d706f35673d3d / RECEIVER Alice
[ RETRIEVE ] RECEIVER Alice / LABEL 4d6d706f35673d3d
[ RETRIEVE ] RECEIVER Bob / LABEL 3562684370413d3d
[ PUBLISH  ] SENDER Alice / LABEL final
[ PUBLISH  ] SENDER Bob / LABEL final
[ RETRIEVE ] RECEIVER Alice. LABEL final / SENDER Bob
[ RETRIEVE ] RECEIVER Bob. LABEL final / SENDER Alice
Alice has finished!
Bob has finished!
Server stopped.
.[ SEND     ] SENDER Alice / LABEL 783156716e773d3d / RECEIVER Bob

...

[ RETRIEVE ] RECEIVER Bob. LABEL final / SENDER Alice
Bob has finished!
Server stopped.
.
test_secret_sharing.py ..

======================= 25 passed in 116.59s (0:01:56) ========================
```

**Note:** You might encounter some warnings when running the tests.
In this case, all of them were related to the libraries used in the project, so
they were not related to the project code by itself.
If you encounter some warning, you might pay attention to them if some relate
to your code, they might reveal some code soon to be obsolete, or some part of
your code that you might want to change.
