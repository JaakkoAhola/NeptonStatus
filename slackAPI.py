#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 13:52:09 2021

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import slack
import aiohttp
import sys

class slackAPI:
    def __init__(self, token, user = None):
        self.token = token
        self.user = user
        
        try:
            self.__connectionWithProxy()
        except aiohttp.client_exceptions.ClientConnectorError:
            try:
                self.__connectionWithout()
            except aiohttp.client_exceptions.ClientConnectorError:
                self.__connectionError()

        assert self.response["ok"]
    
    def __connectionWithProxy(self, proxyinfo = "http://wwwproxy.fmi.fi:8080"):
        self.client = slack.WebClient(token=self.token, proxy = proxyinfo, run_async=False)
        self.response = self.client.api_test()
    
        

    def __connectionWithout(self):
        self.client = slack.WebClient(token=self.token, run_async=False )
        self.response = self.client.api_test()
    
    def __connectionError(self):
        sys.exit("CONNECTION TO SLACK NOT SUCCESSFUL")
        
    
    def __usersHasBeenSet(self):
        assert(self.user is not None)
        
    def getStatus(self):
        self.__usersHasBeenSet()
        
        self.profile = self.client.users_profile_get( user = self.user ).get("profile")
        
        self.currentStatus = self.profile["status_text"]
        
        return self.currentStatus
    
    def setStatus(self, statusDict):
        self.client.users_profile_set(user = self.user, profile = statusDict)