
from setuptools import setup, find_packages

setup(
    name='ai_assistant',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyYAML>=6.0',
        'requests>=2.31.0',
        'openai>=0.27.8',
        'loguru>=0.6.0',
        'pymilvus>=2.2.0',
        'sounddevice>=0.4.6',
        'numpy>=1.21.2',
        'Pillow>=8.3.2',
        'mss>=6.1.0',
        'asyncio',
        'RestrictedPython>=5.1',
        'psutil>=5.8.0',
    ],
    entry_points={
        'console_scripts': [
            'ai-assistant=main:main',
        ],
    },
)
