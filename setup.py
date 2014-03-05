from cx_Freeze import setup, Executable
import sys
# Dependencies are automatically detected, but it might need
# fine tuning.
company_name = 'slg'
product_name = 'pg'

bdist_msi_options = {
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
    'upgrade_code': '{3FD91D28-16DF-45E3-904A-6B65F1D9CBA7}'
    }
buildOptions = dict(packages=[], excludes=['html', 'email', 'socket', 'bz2', 'ssl', 'unicodedate'],
                    include_files=['data/', 'config/'], icon='icon.ico', optimize=2)

base = 'Win32GUI' if sys.platform == 'win32' else None
targetName = 'pg.exe' if sys.platform == 'win32' else 'pg'
version = '0.1.1'
targetName = 'pg-'+version+'.exe'
executables = [
    Executable('main.py', base=base, targetName=targetName, appendScriptToExe=True, compress = True,)
]

setup(name='pg',
      version=version,
      description='simple game test',
      author='Den',
      author_email='denis@ranneft.ru',
      
      options=dict(build_exe=buildOptions, bdist_msi=bdist_msi_options),
      executables=executables)
