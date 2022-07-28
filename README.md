# Identity_server
# HTTP-requests
## api/register
### POST
### input: {
    "login": "any_login",
    "email": "abc@abc.com",
    "password": "xxxxxxxxx"
}
### output: jwt-token

## api/login
### POST
### input: {
    "email": "abc@abc.com",
    "password": "xxxxxxxxx"
}
### output: jwt-token

## api/logout
### POST
### input: jwt-token
### output: "isSuccessful": true

## api/user
### POST
### input: jwt-token
### output: {
    "id": 3,
    "login": "any_login",
    "email": "abc@abc.com"
}
