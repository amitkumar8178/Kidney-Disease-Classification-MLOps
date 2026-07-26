import setuptools

with open("Readme.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.0"

REPO_NAME = "Kidney-Disease-Classification-MLOps"
AUTHOR_USER_NAME = "amitkumar8178"
SRC_REPO = "cnn-classifier"
AUTHOR_EMAIL = "amitkumar8178552618@gmail.com"


setuptools.setup(
   name=SRC_REPO,
   version=__version__,
   author=AUTHOR_USER_NAME,
   author_email=AUTHOR_EMAIL,
   description="A small python package for CNN app",
   long_description=long_description,
   long_description_content="text/markdown",
   url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
   project_urls={
       "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
   }
)