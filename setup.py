from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='ClassAttendanceManager',
    version='1.1',
    description='A simple python script to manage students attendance in class in terminal.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Navid Zarepak',
    author_email='navid2zp@gmail.com',
    url='https://github.com/Navid2zp/ClassAttendanceManager',
    download_url='https://pypi.org/project/ClassAttendanceManager/'
)

if __name__ == '__main__':
    setup(**setup_args,)
