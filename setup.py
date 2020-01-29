import setuptools

try:
    from setuptools import setup
    from setuptools.command.install import install
    from setuptools.command.egg_info import egg_info
except ImportError:
    from distutils.core import setup
import sys
import versioneer

cmdclass = versioneer.get_cmdclass()
version = versioneer.get_version()

if sys.version_info[:2] <= (3, 5):
    raise RuntimeError(
        "You're using Python <= 3.5, but this package requires either Python "
        "3.6 or above, so you can't use it unless you upgrade your "
        "Python version."
    )

dependencies = ['ordered-set', 'pylatex']

extras = {
    'docs': ['sphinx'],
    'matrices': ['numpy'],
    'matplotlib': ['matplotlib'],
    'quantities': ['quantities', 'numpy'],
    'testing': ['flake8<3.0.0', 'pep8-naming==0.8.2',
                'flake8_docstrings==1.3.0', 'pycodestyle==2.0.0',
                'pydocstyle==3.0.0', 'pyflakes==1.2.3', 'nose', 'flake8-putty',
                'coverage'],
}
source_dir = '.'



extras['all'] = list(set([req for reqs in extras.values() for req in reqs]))


class CustomInstall(install):
    def run(self):
        install.run(self)


class CustomEggInfo(egg_info):
    def initialize_options(self):
        egg_info.initialize_options(self)




cmdclass['install'] = CustomInstall
cmdclass['egg_info'] = CustomEggInfo

setup(name='pythonTikz',
      version=version,
      author='Matthew Richards',
      author_email='m.richards2@uq.net.au',
      description='A Python library for creating TikZ LaTeX files and snippets',
      long_description=open('README.rst').read(),
      long_description_content_type='text/x-rst',
      package_dir={'': source_dir},
      # packages=['pythontikz', 'pythontikz.base_classes'],
      packages=setuptools.find_packages(),
      url='https://github.com/m-richards/pythonTikz',
      license='MIT',
      install_requires=dependencies,
      extras_require=extras,
      cmdclass=cmdclass,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux :: Windows',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Code Generators',
          'Topic :: Text Processing :: Markup :: LaTeX',
      ],
      python_requires='>=3.6'
      )
