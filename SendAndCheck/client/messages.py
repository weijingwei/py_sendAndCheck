from configparser import ConfigParser


class Messages(object):
    def __init__(self):
        if not hasattr(self, "messages"):
            print("initial message.properties")
            self.messages = {}
            parser = ConfigParser()  
            parser.read("messages.properties")  
            sections = parser.sections()  
            for section in sections:
                values = parser.items(section)  
                self.messages[section] = values  
    
    def getValue(self, section, option):
        for value in self.messages[section]:
            if value[0] == option:
                return value[1]