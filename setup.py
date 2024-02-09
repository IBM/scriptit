from setuptools import setup, find_packages

setup(
    name='scriptit',
    version='1.0.0',
    description='A collection of tools for writing interactive terminal applications',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Md Sulaiman',
    author_email='infosulaimanbd@gmail.com',
    url='https://github.com/khulnasoft-lab/scriptit',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        # Add any dependencies required by your project here
    ],
    extras_require={
        'dev': [
            'pytest>=6',
            'pytest-cov>=2.10.1',
            'pre-commit>=3.0.4,<4.0',
            'ruff==0.2.0',
            'setuptools>=60',
            'setuptools-scm>=8.0',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
