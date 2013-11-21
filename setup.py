from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-user-sessions',
    version='0.1.1',
    author='Bouke Haarsma',
    author_email='bouke@webatoom.nl',
    packages=find_packages(exclude=('example', 'tests',)),
    package_data={
        'user_sessions': ['templates/user_sessions/*.html'],
    },
    url='http://github.com/Bouke/django-user-sessions',
    description='Django sessions with a foreign key to the user',
    license='MIT',
    long_description=open('README.rst').read(),
    install_requires=['Django>=1.4'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Security',
    ],
)
