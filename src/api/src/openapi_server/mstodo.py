import logging
import json
import msal
import threading
import time
from typing import Union

class MsTodoLifeService:
    def __init__(self, configPath: str):

        self.config = json.load(open(configPath))
        self.pollIntervalSec = self.config["poll_interval_seconds"]
        self.todoList = []
        self.connectMessage = ""

        self.app = msal.PublicClientApplication(
            self.config["client_id"], authority=self.config["authority"]
            )

    def startPolling(self) -> None:
        polling_thread = threading.Thread(target=self._pollWorker)
        polling_thread.daemon = True  # Set as daemon thread
        polling_thread.start()

    def getListByName(self, name: str) -> Union[list,str]:
        if len(self.todoList) == 0:
            return self.connectMessage
        else:
            return self.todoList

    def _pollWorker(self) -> None:
        startTime = time.time()
        self._acquireToken()
        elapsedTime = time.time() - startTime
        time.sleep(max(0, self.pollIntervalSec - elapsedTime))
    
    def _acquireToken(self) -> None:
        
        result = None
        accounts = self.app.get_accounts()
        if accounts:
            if len(accounts) > 1:
                logging.info("Multiple accounts detected in cache. Assuming the first")
            chosen = accounts[0]
            result = self.app.acquire_token_silent(self.config["scope"], account=chosen)
        if not result:
            result = self.app.initiate_device_flow(scopes=self.config["scope"])
            self.connectMessage = result["message"]
            result = self.app.acquire_token_by_device_flow(result)

    