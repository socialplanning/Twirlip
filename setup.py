try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='Twirlip',
    version="0.6",
    description='pylons app for changed-content notifications in opencore',
    author='David Turner',
    author_email='opencore-dev@lists.coactivate.org',
    url='',
    install_requires=["Pylons==0.9.6.2",
                      "signedheaders",
                      "CabochonServer",
                      "simplejson",
                      "wsgi_intercept",
                      "httplib2",
                      "SQLObject",
                      "SupervisorErrorMiddleware",
                      "wsgiutils",
                      "WebOb",
                      ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'twirlip': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'twirlip': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    dependency_links = [
      "https://svn.openplans.org/svn/signedheaders/trunk#egg=signedheaders-dev",
      "https://svn.openplans.org/svn/SupervisorErrorMiddleware/trunk#egg=SupervisorErrorMiddleware-dev",
      ],    
    entry_points="""
    [paste.app_factory]
    main = twirlip.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
