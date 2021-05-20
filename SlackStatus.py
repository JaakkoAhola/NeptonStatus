#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:25:45 2021

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import time
import requests
import os
from slackAPI import slackAPI

import datetime


class SlackStatus(slackAPI):
    def __init__(self, url, user ):
        
        self.user = user
        
        super().__init__(token = os.environ["SLACK_API_TOKEN_NEPTON_STATUS"], user =  self.user)
        
        self.url = url
        
        
        self.statusPool = { "remotework" : {"status_text" : "Presently working remotely @ Pargas",
                                            "status_emoji" : ":parainen:"},
                           "presentwork" : {"status_text" : "Presently working presently @ Dynamicum",
                                     "status_emoji" : ":dynamicum_entrance:"},
                  "free" : {"status_text" : "",
                            "status_emoji": ""},
                  "vacation" :{ "status_text" : "On a vacation",
                               "status_emoji" : ":ocean:"},
                  "sick" : {"status_text": "On a sick leave",
                            "status_emoji" : ":face_with_thermometer:"},
                  "random": {"status_text" : "time slot for random call :slack_call: call me maybe",
                             "status_emoji" : ":arvot_yhteistyo:"},
                  "dayOff": {"status_text" : "Day Off",
                             "status_emoji" : ":balloon:"},
                  "sports" : {"status_text" : "Sports hour",
                             "status_emoji" : ":basketball:"}}
        self.isIt = dict(zip(list(self.statusPool), [False]*len(list(self.statusPool))))
        
        self.default = False

    def getNeptonStatus( self ):
        
        
        response = requests.get( self.url)
        assert(response.status_code == 200)
        # stringi = response.content.decode("UTF-8")
        lines = response.content.decode("UTF-8").replace("\t", "").split("\n")
        
        nykytilaHeaderInd = 0
        for ind,line in enumerate(lines):
            
            if self.__getDataFromHtmlLine(line) == "Nykytila":
                nykytilaHeaderInd = ind
                break
        
        nykytilaInd = nykytilaHeaderInd +1
        
        self.neptonStatus = self.__getDataFromHtmlLine(lines[nykytilaInd])
        
        return self.neptonStatus
    
    def __getDataFromHtmlLine(self, line):
        line = line.replace("</", "_")
        line = line.replace("<", "_")
        line = line.replace(">", "_")
        splitted = line.split("_")
        
        try:
            dataArvo = splitted[2]
        except IndexError:
            dataArvo = None
        
        return dataArvo
        
    def getCurrentTime(self):
        self.dateObj = datetime.datetime.now()
        
        self.dateReadable = self.dateObj.strftime("%Y-%m-%d %H.%M")
    
    def isItTimeForRandomCall(self):
        self.getCurrentTime()
        
        self.isIt["random"] = False
        
        if self.isIt["remotework"] or self.isIt["presentwork"]:
            if self.dateObj.isoweekday() in [1,2,3,4]:
                if self.dateObj.hour == 11 and self.dateObj.minute <= 15:
                    self.isIt["random"] = True
                    
            elif self.dateObj.isoweekday() == 5:
                if (self.dateObj.hour == 10 and self.dateObj.minute >= 30) or (self.dateObj.hour == 11 and self.dateObj.minute < 30):
                    self.isIt["random"] = True
                
        return self.isIt["random"]
    
    def isItRemoteWorking(self):
        
        if self.neptonStatus == "Työ muualla":
            self.isIt["remotework"] = True
        
        return self.isIt["remotework"]
    
    def isItPresentWorking(self):
        
        if self.neptonStatus == "Työ":
            self.isIt["presentwork"] = True
        
        return self.isIt["presentwork"]
    
    def isItSickLeave(self):
        
        if self.neptonStatus == "Sairausloma":
            self.isIt["sick"] = True
        return self.isIt["sick"]
    
    def isItFreetime(self):
        
        if self.neptonStatus == "Vapaalla":
            self.isIt["free"] = True
        return self.isIt["free"]
    
    def isItVacation(self):
        
        if self.neptonStatus == "Vuosiloma":
            self.isIt["vacation"] = True
            
        return self.isIt["vacation"]
    
    def isItDayOff(self):
        if self.neptonStatus == "Saldovapaa":
            self.isIt["dayOff"] = True
        return self.isIt["dayOff"]
    
    def isItSportsHour(self):
        if self.neptonStatus == "Liikuntatunti":
            self.isIt["sports"] = True
        return self.isIt["sports"]
    
    def isDefault(self):
        self.default = False
        if not any( list( self.isIt.values() ) ):
            self.default = True
        return self.default
    
    def checkAndPrintAll(self):
        print(f"Nepton status: {self.getNeptonStatus()}")
        print(f"Remoteworking: {self.isItRemoteWorking()}")
        print(f"Present working: {self.isItPresentWorking()}")
        print(f"Random call: {self.isItTimeForRandomCall()}")
        print(f"Sick leave: {self.isItSickLeave()}")
        print(f"Free time: {self.isItFreetime()}")
        print(f"Vacation: {self.isItVacation()}")
        print(f"Day Off: {self.isItDayOff()}")
        print(f"Sports Day: {self.isItSportsHour()}")
        
    def checkAll(self):
        self.getNeptonStatus()
        
        self.isItTimeForRandomCall()
        self.isItRemoteWorking()
        self.isItPresentWorking()
        
        self.isItSickLeave()
        self.isItFreetime()
        self.isItVacation()
        self.isItDayOff()
        self.isItSportsHour()
        
    def loopTime(self):
        looping = True
        
        self.checkAndPrintAll()
        print()
        
        while looping:
            self.getCurrentTime()
            
            
            
            self.checkAll()
        
        
            while self.isIt["random"]:
                print(self.dateReadable, "random")
                self.setStatus(self.statusPool["random"])
                
                self.getNeptonStatus()
                    
                self.isItTimeForRandomCall()
                    
                time.sleep(60)
                
            
            self.getCurrentTime()
            self.checkAll()
            
            for status in self.isIt:
                if self.isIt[status]:
                    print(self.dateReadable, status)
                    self.setStatus(self.statusPool[status])
            
            if self.isDefault():
                self.setStatus({"status_text" : ""})
            
            time.sleep(60)
            
        

def main():
    slackstatus = SlackStatus( os.environ["NEPTONMOBILE"],
                    os.environ["SLACK_USER_ID"])
    slackstatus.loopTime()
    # slackstatus.setStatus( slackstatus.statusPool["free"] )
    
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    