from utils.log_utils import ServerLogger

SERVER_LOGGER = ServerLogger()
SERVER_LOGGER.log("Start server!")
SERVER_LOGGER.log("Import module ...")
import sys
import signal
import uvicorn
import traceback
from llm_api.interface_api import FastApiInterface

SERVER_LOGGER.log("Import module done ")

def signal_handler(sig, frame):
    SERVER_LOGGER.log("Kill program by Ctrl + C")
    sys.exit(0)

if __name__ == "__main__":
    SERVER_LOGGER.log("Initializing API...")
    signal.signal(signal.SIGINT, signal_handler)

    try:
        fi = FastApiInterface()
        fi.start_routers()
        SERVER_LOGGER.log("\n")
        SERVER_LOGGER.log(
            r"        *********************              <-|->             *********************"
        )
        SERVER_LOGGER.log(
            r"        *                                                                        *"
        )
        SERVER_LOGGER.log(
            r"        *                       Ready to use API ~(^.^)~                         *"
        )
        SERVER_LOGGER.log(
            r"        *                                                                        *"
        )
        SERVER_LOGGER.log(
            r"        *********************              <-|->             *********************"
        )
        SERVER_LOGGER.log("\n")

        uvicorn.run(fi.app)
    except Exception as e:
        SERVER_LOGGER.log(f"Main error : {e}")
        SERVER_LOGGER.log(f"\n=> {traceback.format_exc()}")

    finally:
        SERVER_LOGGER.log("Shutdown server, goodbye!")
