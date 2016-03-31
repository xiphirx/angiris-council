from setuptools import setup

setup(name='angiriscouncil',
	  version='1.1',
	  description='A collection of bots to perform moderation tasks on r/Diablo',
	  url='https://www.reddit.com/r/Diablo',
	  author='Hilal Alsibai',
	  license='GPLv3',
	  packages=['angiriscouncil'],
	  install_requires=['praw', 'pytz'],
	  zip_safe=False)
