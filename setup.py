from setuptools import setup, find_packages

setup(
    name="wfmplan",
    version="0.2.1",
    description=" tools for workforce management optimization",
    url="https://github.com/laddha-rishi/wfmplan",
    author="Rishi Laddha",
    author_email="laddha.rishi@gmail.com",
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    project_urls={
        "Source Code": "https://github.com/laddha-rishi/wfmplan"
    },
    packages=find_packages(include=['wfmplan', 'wfmplan.*']),
    install_requires=[
        'numpy>=1.23.0',
        'pandas>=1.3.5',
    ],
    include_package_data=True,
) 