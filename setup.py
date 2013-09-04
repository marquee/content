from setuptools import setup

setup(
        name                = 'droptype-content',
        version             = 'dev',
        description         = '',
        long_description    = file('README.md').read(),
        url                 = 'https://github.com/droptype/content',
        author              = 'Alec Perkins',
        author_email        = 'alec@droptype.com',
        license             = 'UNLICENSE',
        packages            = ['content'],
        zip_safe            = False,
        keywords            = '',
        install_requires    = file('requirements.txt').read().splitlines(),
        classifiers         = [
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: Public Domain',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    )