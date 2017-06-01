
import sys

from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

assert sys.version_info >= (2, 6), "We only support Python 2.6+"

install_requires = [
    'urllib3',
    'requests>=2.5.1,!=2.6.1',
    'six>=1.3.0',
    'requests_toolbelt>=0.7.0'
]

tests_require = [
    'pytest',
    'requests',
    'tornado'
]

setup_requires = [
    'pytest-runner'
]

setup(
        name='fangcloud',
        version='2.2.3',
        description='Official YiFangYun SDK for Open Platform',
        author='YiFangYun',
        author_email='linrenjun@yifangyun.com',
        maintainer='linrenjun',
        maintainer_email='lrenjundk@foxmail.com',
        url='https://www.yifangyun.com',
        install_requires=install_requires,
        tests_require=tests_require,
        setup_requires=setup_requires,
        zip_safe=False,
        packages=['fangcloud'],
        package_data={'fangcloud': ['trusted-certs.crt']},
        # py_modules=['fangcloud'],
        classifiers=classifiers,
        platforms=["all"],
        keywords='yifangyun api sdk',
        license='Apache Software License, Version 2.0, http://www.apache.org/licenses/LICENSE-2.0'
)


