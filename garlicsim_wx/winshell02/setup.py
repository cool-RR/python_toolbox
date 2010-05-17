from distutils.core import setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Environment :: Win32 (MS Windows)',
  'Intended Audience :: Developers',
  'Intended Audience :: System Administrators',
  'License :: PSF',
  'Natural Language :: English',
  'Operating System :: Microsoft :: Windows :: Windows 95/98/2000',
  'Topic :: System :: Systems Administration'
]

setup (
  name = "winshell",
  version = "0.2",
  description = "Windows shell functions",
  author = "Tim Golden",
  author_email = "mail@timgolden.me.uk",
  url = "http://timgolden.me.uk/python/winshell.html",
  license = "http://www.opensource.org/licenses/mit-license.php",
  py_modules = ["winshell"]
)

