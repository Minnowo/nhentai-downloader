
import os
import sys

from logger import logger

class CMD_Command():

    def __init__(self, command : str, arg_type : str, callback):
        
        self.command = command
        self.arg_type = arg_type
        self.callback = callback
        self.has_value = arg_type != "None" and arg_type



class CMD_Parser():

    def __init__(self):
        self.coms = {}


    def _Handle_Arg(self, arg, value=None):
        
        if not value:
            arg.callback()
            return
        
        if arg.arg_type == "int":
            arg.callback(int(value))

        elif arg.arg_type == "str":
            arg.callback(str(value))


    def Parse_Coms(self, args):

        if not isinstance(args, list):
            return

        con = False
        try:
            for i in range(len(args)):

                if con:
                    con = False
                    continue

                if args[i] in self.coms:

                    if self.coms[args[i]].has_value:
                        self._Handle_Arg(self.coms[args[i]], args[i + 1])
                        con = True
                        continue

                    else:
                        self._Handle_Arg(self.coms[args[i]])
                        continue

                logger.critical("Invalid argument: %s" % args[i])
                quit(1)
        except IndexError as e:
            pass


    def Add(self, cmd : CMD_Command):
        
        if cmd not in self.coms:
            self.coms[cmd.command] = cmd


    def Remove(self, command : str):

        del self.coms[str(command)]
