from setuptools import setup, find_namespace_packages

setup(
    name='pco_checker',
    use_scm_version=True,
    description='Checks Planning Center for unfilled positions in upcoming services',
    author='James Muscat',
    author_email='jamesremuscat@gmail.com',
    url='https://github.com/jamesremuscat/pco-checker',
    packages=find_namespace_packages('src', exclude=["*.tests"]),
    package_dir={'': 'src'},
    setup_requires=['setuptools_scm'],
    tests_require=[],
    install_requires=[
        'colorama',
        'jsonapi_requests',
        'tenacity==7.0.0'
    ],
    entry_points={
        'console_scripts': [
            'pco_checker=pco_checker.__main__:run'
        ],
    }
)
