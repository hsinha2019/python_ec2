from setuptools import setup

setup(
	name='EC2 with Python',
	version='0.1',
	author='Himanshu Sinha',
	license='GPLv3+',
	packages=['ec2'],
	install_requires=['click','boto3','botocore'],
	entry_points='''
		[console_scripts]
		hello=ec2.listEC2:cli''',
)