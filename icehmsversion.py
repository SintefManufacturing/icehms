
from bzrlib.branch import Branch
branch = Branch.open(".")
VERSION = "0.8.2" + "-bzr-" + branch.nick + "-rev" + str(branch.revno())
