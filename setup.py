from setuptools import setup, find_packages

setup(
    name='qrsave',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Pillow',
        'qrcode'
    ],
    entry_points='''
        [console_scripts]
        qrsave=qrsave.cli:qrsave
    ''',
)
