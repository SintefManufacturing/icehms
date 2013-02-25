import logging

import icehms
import test1, test2
import message1, message2
import publisher, subscriber
import custom_interface1, custom_interface2

if __name__ == "__main__":
    
    mgr = icehms.AgentManager("Testing_all", logLevel=logging.DEBUG)
    try:

        holon = test1.TestHolon("Holon1", logLevel=logging.INFO)
        holon.other = ("Holon2")
        mgr.add_holon(holon)
        holon = test2.TestHolon("Holon2", logLevel=logging.INFO)
        holon.other = ("Holon1")
        mgr.add_holon(holon)

        holon = message1.TestHolon("Message1", logLevel=logging.INFO)
        holon.other = ("Message2")
        mgr.add_holon(holon)
        holon = message2.Client("Message2", logLevel=logging.INFO)
        mgr.add_holon(holon)

        holon = publisher.Server("TestPublisher", logLevel=logging.INFO)
        mgr.add_holon(holon)
        holon = subscriber.Client("TestClient", logLevel=logging.INFO)
        mgr.add_holon(holon)


        holon = custom_interface1.TestHolon("CustomHolonClient", logLevel=logging.INFO)
        mgr.add_holon(holon)
        holon = custom_interface2.TT("CustomHolon", logLevel=logging.INFO)
        mgr.add_holon(holon)
        #from IPython.frontend.terminal.embed import InteractiveShellEmbed
        #ipshell = InteractiveShellEmbed( banner1="\n\n  robot object is available  \n\n")
        #ipshell(local_ns=locals())
    except:
        mgr.shutdown()
        raise
    else:
        mgr.wait_for_shutdown()





