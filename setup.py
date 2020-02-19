from setuptools import setup

classifiers = [
                  'Development Status :: 5 - Production/Stable',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: Apache Software License',
                  'Operating System :: POSIX',
                  'Operating System :: MacOS :: MacOS X',
                  'Topic :: Software Development :: Testing',
                  'Topic :: Software Development :: Libraries',
                  'Topic :: Utilities',
              ] + [
                  ('Programming Language :: Python :: %s' % x) for x in '3 3.3 3.4 3.5 3.6 3.7 3.8'.split()
              ]

with open('README.rst') as read_me:
    long_description = read_me.read()

setup(
    name='nimoy-framework',
    version='1.0.1',
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
    install_requires=['pyhamcrest==2.0.0', 'urllib3==1.25.8'],
)
