init -10 python:
        
    
    # First part of working with databases - Autoclass
    # Universal structure for data
    class Structure(_object):
        def __init__(self, namespace=None):
            self.flags = []
            if namespace:
                for key in namespace:
                    self.set(key,namespace[key])
        def get(self, par):
            return self.__dict__[par]

        def namespace(self):
            return self.__dict__

        def has(self, par):
            return self.__dict__.has_key(par)

        def set(self, par, value):
            self.__dict__[par] = value

        def mod(self, par, value):
            self.__dict__[par] += value

        def flag(self, flag):
            return flag in self.flags

        def setflag(self, flag):
            if flag not in self.flags:
                self.flags.append(flag)

        def delflag(self, flag):
            if flag in self.flags:
                self.flags.remove(flag)

    # Conversion of xml into multileveled dictionary, up to 4 levels
    # Special requirement: Nodes must have different names and have id as an attribute that will be used as a key
    # Otherwise the resulting dictionary will contain only the last node as they will rewrite eachother
    # Conversation: Every Node = Dictionary. To access sublevels
    # access them as an included dictionary
    # to gain access to attribute - access the dictionary attr inside the required node

    # "db/buildings.xml" - result['smallbrothel1']['small']['attr']['type'] will return 'empty'
    def xml_to_dict(filename):
        tree = ET.parse(filename).getroot()
        result = parse_xml_node(tree)
        return result
        
    def parse_xml_node(node):
        result = {}
        for n in node:
            if n.attrib.has_key('id'):
                n.tag = n.attrib['id']

            result[n.tag] = dict(attr = n.attrib)
            for key in result[n.tag]:
                result[n.tag][key] = parse(result[n.tag][key])

            result[n.tag].update(parse_xml_node(n))

        return result

    # Second part of the engine to work databases
    # loading and xml file into a dictionary
    def dict_from_config_file(file, raw=False, vars=None):
        result = dict()
        tree = ET.parse(file).getroot()
        for node in tree:
            # Compability with Crazy mod again:
            if "Name" in node.attrib:
                if not node.attrib.has_key('id'): node.attrib['id'] = node.attrib["Name"]
            if not node.attrib.has_key('id'): node.attrib['id'] = node.tag
            result[node.attrib['id']] = node.attrib
            result[node.attrib['id']]['xml'] = node
        return result

    # Third part of engine to work databases
    # Uses parse function
    # Parameters:
    # entity - class to be used
    # preform_init - whether to run init() after loading object
    def load_database(file, entity=Structure, perform_init=False):
        db = dict_from_config_file(file)
        dictionary = dict()
        for entry in db:
            dictionary[entry] = entity()
            if entity == Char:
                Stats = dictionary[entry].STATS
                Skills = dictionary[entry].stats.skills.keys()
                # Had to change quite a bit to allow crazies packs into the game...
                for key in db[entry]:
                    if key.lower() == "blowjob":
                        skill = "oral"
                    elif key.lower() == "normalsex":
                        skill = "vaginal"
                    else:
                        skill = key
                    if skill.lower() in Skills:
                        value = parse(db[entry][key])
                        setattr(dictionary[entry], skill.lower(), value * (2/3.0))
                        setattr(dictionary[entry], skill.capitalize(), value * (1/3.0))
                    if key.lower() in Stats:
                        if key != "luck":
                            value = parse(db[entry][key])
                            key = key.lower()
                            value = int(round(float(value)*dictionary[entry].get_max(key))/100)
                            dictionary[entry].mod_stat(key, value)
                        elif key == "luck":
                            value = parse(db[entry][key])
                            key = key.lower()
                            dictionary[entry].mod_stat(key, value)
                        else:
                            raise Exception, "During loading of unique girls in load_database function. key.lower() = %s"%key
                    elif key == "Desc":
                        dictionary[entry].__dict__["desc"] = parse(db[entry][key])
                    elif key == "location":
                        dictionary[entry].location = parse(db[entry][key])
                    else:
                        if key[0].isupper() and not key.startswith("Tr"):
                            pass
                        else:
                            dictionary[entry].__dict__[key] = parse(db[entry][key])
                    dictionary[entry].id = entry
            else:    
                for key in db[entry]:
                    dictionary[entry].__dict__[key] = parse(db[entry][key])
                    dictionary[entry].id = entry

        if perform_init:
            for entry in dictionary:
                dictionary[entry].init()

        return dictionary
