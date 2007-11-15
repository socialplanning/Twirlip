try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='Twirlip',
    version="",
    #description='',
    #author='',
    #author_email='',
    #url='',
    install_requires=["Pylons>=0.9.6.1",
                      "cookieauth",
                      "CabochonServer",
                      "simplejson",
                      "wsgi_intercept==httplib2,>=0.3dev",
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
      "http://wsgi-intercept.googlecode.com/svn/branches/httplib2/#egg=wsgi_intercept-httplib2",
      "https://svn.openplans.org/svn/cookieauth/trunk",
      ],    
    entry_points="""
    [paste.app_factory]
    main = twirlip.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
