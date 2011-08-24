try:
    from bzrlib.branch import Branch
except ImportError:
    bzrstring = ""
else:
    branch = Branch.open(".")
    rev = str(branch.revno())
    nick = branch.nick
    bzrstring = "-bzr-" + nick + "-rev" + rev
VERSION = "0.8.5" + bzrstring
