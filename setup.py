from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="wfmplan",
    version="1.2.1",
    description="Optimization library for workforce management planning",
    long_description=long_description,
    long_description_content_type='text/markdown',
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
        "Source Code": "https://github.com/laddha-rishi/wfmplan",
        "Documentation": "https://medium.com/@laddha.rishi/queueing-up-success-revolutionize-workforce-planning-with-python-6c9d7edbb6cd",
    },
    packages=find_packages(include=['wfmplan', 'wfmplan.*']),
    install_requires=[
        'numpy>=1.23.0',
        'pandas>=1.3.5',
    ],
    include_package_data=True,
    keywords="workforce management optimization",
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'wfmplan=wfmplan:main',
        ],
    },
)
