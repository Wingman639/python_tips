*** Settings ***
Library    call_func_as_keyword.py
Library    run_as_keyword.py

*** Test Cases ***
Say Hello Cases
    show_hello

Say Good Morning
    show_good_morning


*** Keywords ***