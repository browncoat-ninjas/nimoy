from setuptools import setup

classifiers = [
                  'Development Status :: 4 - Beta',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: Apache Software License',
                  'Operating System :: POSIX',
                  'Operating System :: MacOS :: MacOS X',
                  'Topic :: Software Development :: Testing',
                  'Topic :: Software Development :: Libraries',
                  'Topic :: Utilities',
              ] + [
                  ('Programming Language :: Python :: %s' % x) for x in '3 3.3 3.4 3.5 3.6'.split()
              ]

with open('README.rst') as read_me:
    long_description = read_me.read()

setup(
    name='nimoy-framework',
    version='0.0.1b6',
    description='A testing and specification framework for Python 3, heavily inspired by the Spock Framework',
    long_description=long_description,
    url='https://github.com/browncoat-ninjas/nimoy',
    license='Apache License',
    platforms=['unix', 'linux', 'osx'],
    author='Noam Tenne, Yoav Luft',
    author_email='noam@10ne.org',
    entry_points={'console_scripts': ['nimoy = nimoy.main:main']},
    classifiers=classifiers,
    keywords="test unittest specification",
    packages=['nimoy', 'nimoy.assertions', 'nimoy.ast_tools', 'nimoy.context', 'nimoy.runner', 'nimoy.compare'],
    install_requires=['pyhamcrest==1.9.0'],

)
