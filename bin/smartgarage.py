#!/usr/bin/env python

# import SmartGarage.smartgarage
import ConfigParser

configfile = "smartgarage.ini"

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
	    if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

config = ConfigParser.ConfigParser()
config.read(configfile)

print config.sections()

if __name__ == "__main__":
    
