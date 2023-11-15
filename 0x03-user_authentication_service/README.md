# User authentication service
![img](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2019/12/4cb3c8c607afc1d1582d.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20231113%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231113T035726Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=5732e11a31d90207766594e032c7f6329e46a607c4bcf6259e2eebda78428bbe)

In the industry, you should not implement your own authentication system and use a module or framework that doing it for you (like in Python-Flask: [Flask-User](https://flask-user.readthedocs.io/en/latest/api.html)). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

## Resources
### Read or watch:
- [Flask documentation](https://flask.palletsprojects.com/en/2.3.x/quickstart/)
- [Requests module](https://requests.kennethreitz.org/en/latest/user/quickstart/)
- [HTTP status codes](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)

## Learning Objectives
- How to declare API routes in a Flask app
- How to get and set cookies
- How to retrieve request form data
- How to return various HTTP status codes

## Requirements
- You should use SQLAlchemy 1.3.x
- The flask app should only interact with `Auth` and never with `DB` directly.
- Only public methods of `Auth` and `DB` should be used outside these classes

## Setup
You will need to install `bcrypt`
```
pip3 install bcrypt
```

