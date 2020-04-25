from setuptools import setup

setup(name='stocklights',
      version='0.1',
      description='App to watch your stock portfolio and change a light color depending on gains or losses',
      url='http://github.com/HaakenJ/StockLights',
      author='HaakenJ',
      author_email='haaken1234@gmail.com',
      license='MIT',
      packages=['stocklights'],
      install_requires=[
            'requests',
            'mysql-connector-python'
      ],
      zip_safe=False)
