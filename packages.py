#https://docs.python.org/3/library/subprocess.html
import subprocess
import sys

packages = [
    'pandas',
    'numpy',
    'scikit-learn',
    'matplotlib'
]

for p in packages:
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', p], check=True)
        print(f'{p} installed.\n')
    except subprocess.CalledProcessError as e:
        print(f'error installing {p}: {e}')
        sys.exit(1)  
