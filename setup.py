from setuptools import setup,find_packages
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    requirements=[]
    "This function will return a list of requirements"
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
    requirements=[req.replace('/n','') for req in requirements]
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT) 
    return requirements
    
    

setup(
    name='Student_Exam_Performance',
    version='1.0',
    description='A Python package for managing data.',
    author='Shyam',
    author_email='sirapurapushyam@gmail.com',
    url='https://github.com/Shyam1719/Student_Exam_Performance',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

