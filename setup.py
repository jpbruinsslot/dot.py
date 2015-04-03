try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

README = open('README.rst').read()
CHANGES = open('CHANGES.rst').read()

setup(
    name='dot',
    description='Simple Dotfiles Tracking',
    long_description=README + '\n' + CHANGES,
    author='erroneousboat',
    author_email='erroneousboat@gmail.com',
    url='http://www.erroneousboat.com',
    version='0.1b3',
    license='MIT',
    install_requires=['nose', 'docopt'],
    packages=['dot'],
    scripts=['bin/dot'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License'
    ]
)
