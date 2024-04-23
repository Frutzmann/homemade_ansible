from setuptools import setup
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='hma',
    version='0.0.1',
    packages=['homemade_ansible', 'homemade_ansible.logger', 'homemade_ansible.static', 'homemade_ansible.modules',
              'homemade_ansible.connections'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'hma=homemade_ansible.homemade_ansible:main',
        ],
    },
    url='https://github.com/Marcoulin/homemade_ansible',
    license='',
    author='François UTZMANN',
    author_email='utzmann.francois@gmail.com',
    description='Home Made Ansible'
)
