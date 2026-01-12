from setuptools import setup, find_packages
import os
from typing import List

def get_requirements()->List[str]:
    """ this function returns the list of requirements

    """
    requirement_list:List[str] =[]
    try:
        with open('requirements.txt','r') as f:
            lines =f.readlines()
            for line in lines:
                requirement =line.strip()
                ##ignore empty lines and comments

                if requirement and requirement!='-e .':
                    requirement_list.append(requirement)
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")
    return requirement_list

setup(
    name = 'NetworkSecurity',
    version = '0.0.0',
    author ='Uday Singh',
    author_email ='udaysingh.288@gmail.com',
    packages= find_packages(),
    install_requires = get_requirements()
     )