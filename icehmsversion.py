try:
    from bzrlib.branch import Branch
except ImportError:
    rev = "Unknown"
    nick = "icehms"
else:
    branch = Branch.open(".")
    rev = str(branch.revno())
    nick = branch.nick
VERSION = "0.8.3" + "-bzr-" + nick + "-rev" + rev
