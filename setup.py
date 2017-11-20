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

setup(name='usgs_wma_mlr_ddot_ingester',
      version='0.4.0dev',
      description='MLR Ddot Ingester Microservice',
      author='Mary Bucknell, Andrew Yan, Dave Steinich, Zack Moore, Kathy Schoephoester',
      author_email='mlr-devs@usgs.gov',
      include_package_data=False,
      long_description =read('README.md'),
      install_requires=requirements,
      test_loader='unittest:TestLoader',
      platforms='any',
      zip_safe=False,
      py_modules=['app', 'config', 'services', 'ddot_utils', 'flask_restplus_jwt']
      )