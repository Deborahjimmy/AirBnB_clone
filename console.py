#!/usr/bin/python3
"""
Script contains the entry point of the command interpreter
"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Console
    Defines all the commands for the console interpreter
    args:
        cmd.Cmd - commad class
    """
    prompt = "(hbnh) "
    cls_names = ["BaseModel", "User",
                 "Place", "City", "State",
                 "Amenity", "Review"]

    def do_count(self, line):
        """Prints number of object in a class
        args:
            line: object name
        Usage: count <obj_name>
        """
        if line:
            if line in HBNBCommand.cls_names:
                count = 0
                for obj in storage.all().keys():
                    if line in obj:
                        count += 1
                print(count)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_quit(self, arg):
        """Command exit the program"""
        raise SystemExit

    def emptyline(self):
        pass

    def do_EOF(self, line):
        """Ends Code"""
        return True

    def do_create(self, cls_name):
        """Creates a new object
        Usage: create <object_name>
        """
        if not cls_name:
            print("** class name missing **")
        elif cls_name in HBNBCommand.cls_names:
            new_class = eval(cls_name + "()")
            new_class.save()
            print(new_class.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Search if object exits using id
        Args:
            line - object properties
        Usage: show <object_name> <object_id>
        """
        res_line = HBNBCommand.arg_checker(line)
        if res_line != ():
            print(res_line)
            if res_line[1] in res_line[0].keys():
                print(res_line[0][res_line[1]])
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """Deletes a object if it exits using id
        Args:
            line - object properties
        Usage: destroy <object_name> <object_id>
        """
        res_line = HBNBCommand.arg_checker(line)
        if res_line != ():
            if res_line[1] in res_line[0].keys():
                res_line[0].pop(res_line[1])
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        """Displays all object if it exists
        Args:
            line (optional) - object name
        Usage: all or all <object_name>
        """
        if line:
            line_dict = []
            for key, value in storage.all().items():
                if line in key:
                    line_dict.append(str(value))
            if line_dict:
                print(line_dict)
            else:
                print("** class doesn't exist **")
        else:
            print([str(i) for i in storage.all().values()])

    def do_update(self, line):
        '''Updates details of an object
        Agrs:
            line - object properties
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        '''
        res_line = HBNBCommand.arg_checker(line)
        if res_line:
            cls_dict, cls_name_id = res_line
            if cls_name_id in cls_dict.keys():
                line_split = [i.strip('"') for i in line.split(" ", 3)]
                if len(line_split) >= 3:
                    if len(line_split) == 4:
                        try:
                            line_split[3] = eval(line_split[3])
                        except Exception:
                            pass
                        setattr(cls_dict[cls_name_id],
                                line_split[2],
                                line_split[3])
                        storage.save()
                    else:
                        print("** value missing **")
                else:
                    print("** attribute name missing **")
            else:
                print("** no instance found **")

    @staticmethod
    def arg_checker(line):
        """
        Checks validity if input
        Args:
            line (string) - command arguements
        """
        list_line = line.split()
        if not list_line:
            print("** class name missing **")
        elif list_line[0] not in HBNBCommand.cls_names:
            print("** class doesn't exist **")
        elif len(list_line) < 2:
            print("** instance id missing **")
        else:
            storage.reload()
            cls_name_id = list_line[0] + "." + list_line[1]
            cls_dict = storage.all()
            return cls_dict, cls_name_id
        return ()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
