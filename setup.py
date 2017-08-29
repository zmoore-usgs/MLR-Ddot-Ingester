from setuptools import setup


def read_requirements(filename):
    """
    Get application requirements from
    the requirements.txt file.
    :return: portal_ui Python requirements
    :rtype: list
    """
    with open(filename, 'r') as req:
        requirements = req.readlines()
    install_requires = [r.strip() for r in requirements if r.find('git+') != 0]
    return install_requires


def read(filepath):
    """
    Read the contents from a file.
    :param str filepath: path to the file to be read
    :return: file contents
    :rtype: str
    """
    with open(filepath, 'r') as f:
        content = f.read()
    return content



requirements = read_requirements('requirements.txt')
test_requirements = read_requirements('test_requirements.txt')

setup(name='usgs_wma_mlr_ddot_ingester',
      version='0.1.0dev',
      description='MLR Ddot Ingester Microservice',
      author='Mary Bucknell, Andrew Yan, Dave Steinich, Zack Moore, Kathy Schoephoester',
      author_email='mlr-devs@usgs.gov',
      include_package_data=False,
      long_description =read('README.md'),
      install_requires=requirements,
      test_suite='nose.collector',
      test_requires=test_requirements,
      platforms='any',
      zip_safe=False,
      py_modules=['app', 'config', 'services', 'ddot_utils']
      )