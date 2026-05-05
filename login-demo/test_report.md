# Automated Test Report

Generated Time: 2026-05-05 15:25:21.770667

## PRD Rule
Username length must be greater than 6 characters.

## Test Results

### TC_REG_001 - Username length should be greater than 6 characters
- Input: {'username': 'abc123', 'password': '12345678'}
- Expected Status: 400
- Actual Status: 200
- Actual Response: {'message': 'Register success'}
- Result: FAIL

## Auto Generated Bug
- Bug Title: Registration allows username shorter than required length
- Severity: High
- Description: According to the PRD, the username length must be greater than 6 characters. However, the system allows registration with username 'abc'.
- Expected Result: Registration should fail because username length is not greater than 6.
- Actual Result: Status Code: 200, Response: {'message': 'Register success'}
