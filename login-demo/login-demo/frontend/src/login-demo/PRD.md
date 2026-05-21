
# Login and Registration System PRD

## 1. Project Overview

This system provides basic user registration and login functions. Users can create an account with a username and password, and then log in with the registered credentials.

After successful login, the system only needs to show a simple welcome message.

## 2. Registration Requirements

1. The username cannot be empty.
2. The username length must be greater than 6 characters.
3. The password cannot be empty.
4. The password length must be greater than 6 characters.
5. If the username already exists, registration should fail.
6. If all information is valid, registration should succeed.

## 3. Login Requirements

1. The username cannot be empty.
2. The password cannot be empty.
3. Users can log in only when the username and password are correct.
4. If the username or password is incorrect, login should fail.
5. After successful login, the system should return a welcome message.

## 4. Expected Login Success Response

When login is successful, the system should return:

{
  "message": "Login success",
  "data": "Welcome! You have successfully logged in."
}

## 5. Intentional Bug for Testing Demo

According to the PRD, the username length must be greater than 6 characters.

However, the backend system intentionally does not validate username length during registration.

This means a username such as "abc" can still be registered successfully.

This is an intentional bug for demonstrating automated PRD-based testing.
