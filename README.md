# vending_machine
API for a vending machine, with a “seller” and “buyer” role.

# Prerequisites
You'll need the following:
* [Python (3.7)]

### Virtualenv
Make a Python 3 virtualenv

> We recommend using the latest version of Python 3, you should at least use Python 3.7.

```shell
$ python -m venv venv
$ source venv/bin/activate
```

# Set up the local 

1. Clone the project from the repo.

2. You have to install the dependencies listed in the [requirements.txt] to run it locally. It is advisable to 
creat a virtual env first .
  ```
pip install -r requirements.txt
  ```

3. Run below command in the shell to see the input and output.
```
python manage.py 
```
Visit port in the browser
```
http://localhost:8000/docs/
```
4. To run the tests run below command
```
pytest
```

# For Docker container

Run the following cmds in the terminal once the project it set up in local.
```
docker-compose build
```
```
docker-compose up
```

Then visit the port in the browser to see the endpoints:
```
http://localhost:8000/docs/