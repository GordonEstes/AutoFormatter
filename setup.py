from distutils.core import setup
import py2exe

# setup(
#     windows=[{'script': 'AutoFormatter.py'}],
#     options={
#         'py2exe': 
#         {
#             'includes': ['lxml.etree', 'lxml._elementpath', 'gzip', 'docx'],
#         }
#     }
# )

main_script = "AutoFormatter"


# data_files = [
#     ('templates', ['C:\Python27\Lib\site-packages\python_docx-0.8.5-py2.7.egg\docx\\templates']), 
# ]

setup(
    options={
    	'py2exe': 
        {
            'includes': ['lxml.etree', 'lxml._elementpath', 'gzip', 'docx'],
        }
    },
    zipfile=None,
    windows=[{'script': '%s.py' %(main_script)}],
    # data_files=data_files
)