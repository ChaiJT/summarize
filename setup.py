from setuptools import setup

setup(name="summarize",
      version="1.0",
      description="A NLP tool, extract keywords and summary from text.",
      author="Chai",
      python_requires=">=3.6.0",
      license="MIT License",
      packages=["summarize"],
      package_dir={"summarize": "summarize"},
      package_data={"summarize":["*.*"]},
      install_requires=["pkuseg", "jieba", "numpy", "networkx"]
      )
