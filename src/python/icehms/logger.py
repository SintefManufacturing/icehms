from icehms import hms


class Logger(object):
    """
    Simple logger class for icehms
    parameters:
    parent is used to identify logger
    identifier is an arbitrary string 
    logLevel
    """
    def __init__(self, parent, identifier, logLevel):
        self.parent = parent
        self.identifier = identifier
        self._logLevel = logLevel
        self._logPub = None
        self._logFile = None
        self._logToFile = False
        self._logToStdout = True
        self._logToTopic = False
        self.icemgr = None

    def setLogLevel(self, level, ctx=True):
        self._logLevel = level
 
    def enableLogToTopic(self, current=None):
        """
        Enable logging to a topic
        """
        self._logToTopic = True
        if self.icemgr:
            self._createLogPub()

    def _createLogPub(self):
        self._logPub = self.icemgr.getPublisher("Log:" + self.identifier, hms.LogMonitorPrx, server=None)

    def disableLogToTopic(self, current=None):
        """
        Stop logging to a topic
        """
        self._logToTopic = False

    def log(self, msg, level=6):
        """
        log to enabled channels 

        0 Emergency: system is unusable
        1 Alert: action must be taken immediately
        2 Critical: critical conditions
        3 Error: error conditions
        4 Warning: warning conditions
        5 Notice: normal but significant condition
        6 Informational: informational messages
        7 Debug: debug-level messages
        """
        if type(level) != int:
            self._log("self._log called with wrong argument !!!", 1)
            level = 1
        if level <= self._logLevel:
            self._log(msg, level)


    def ilog(self, *args, **kwargs):
        """
        format everything to string before logging
        """
        msg = ""
        if kwargs.has_key("level"):
            level = kwargs["level"]
        else:
            level = 6
        for arg in args:
            msg += " " + str(arg)
        self.log(msg, level)

    def _log(self, msg, level):
        """
        internal , used by logging functions
        """
        msg = str(level) + "::" + self.parent.__class__.__name__ + "::" + self.identifier + ": " + str(msg)
        if self._logToStdout:
            print(msg)
        if self._logToTopic:
            if not self._logPub and self.icemgr:
                self._createLogPub()
            if self._logPub:
                try:
                    self._logPub.appendLog(msg)
                except Ice.Exception:
                    print "Exception when publishing to topic, check topic manager"
        if self._logToFile:
            self._logFile.write(msg + "\n")

    def enableLogToStdout(self, ctx=None):
        self._logToStdout = True

    def disableLogToStdout(self, ctx=None):
        self._logToStdout = False

    def enableLogToFile(self, ctx=None):
        if not self._logToFile:
            try:
                self._logFile = open("Trace_"+ self.identifier + "_" + str(time()) + ".txt", "w")
            except IOError, why:
                self.ilog("Error opening log file: ", why)
                return False
            self._logToFile = True
        return True

    def disableLogToFile(self, ctx=None):
        self._logToFile = False

    def cleanup(self):
        if self._logToFile:
            self._logFile.close()


