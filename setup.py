from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-user-sessions',
    version='0.1.0-beta',
    author='Bouke Haarsma',
    author_email='bouke@webatoom.nl',
    packages=find_packages(exclude=('demo', 'tests',)),
    package_data={
        'user_sessions': ['templates/user_sessions/*.html'],
    },
    url='http://github.com/Bouke/django-user-sessions',
    description='User sessions for Django',
    license='MIT',
    long_description=open('README.rst').read(),
    install_requires=['Django>=1.4'],
    classifiers=[
        'Development Status :: 4 - Beta',
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
