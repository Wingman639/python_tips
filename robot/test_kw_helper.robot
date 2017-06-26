*** Settings ***
Library    say_something.py

*** Test Cases ***
Say Good Morning
    ${TIME}     say_hello

Say Good Afternoon
    ${TIME}     say_hello

Say Good Evening
    ${TIME}     say_hello

*** Keywords ***