# CAM-NLU
A module/extension to extract objects and aspects from natural language.

## Introduction

This Project aims to provide CAM (Comparative Argumentative Machine, Language Techonology Group, UHH)
with the ability to understand natural language. The goal is that CAM can extract objects and aspects of a comparative question
and tell if a question is not comparative. 

## Technologies

This project uses the following technologies:   
-Python 3.10.9   
-spaCy  
-flask  
-Bootstrap 5.3.0-alpha1  
-waitress  
-miniconda3  

## Installation

## Launching the programm

## Architecture 

The program is started with the serv.py file. This file uses flask and waitress to provide a user interface at localhost:5000. 
serv.py imports the class Extractor, located in the file CAM_NLU.py and uses two of its functions, extract_comparative and check_comparative. 
