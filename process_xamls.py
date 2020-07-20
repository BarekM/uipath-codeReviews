import os
import re


import xml.etree.ElementTree as ET


class Variable():
    
    datatype = ''
    name = ''
    scope = ''
    default_value = ''
    
    xaml_variable = None
    
    def __get_name(self):
        self.name = self.xaml_variable.attrib['Name']
    
    def __get_type(self):
        t = self.xaml_variable.attrib['{http://schemas.microsoft.com/winfx/2006/xaml}TypeArguments']
        p = 'x:(\w+)'
        reg = re.compile(p)
        r = reg.search(t)
        t = r.group(1)
        self.datatype = t
    
    def __init__(self, xaml_variable):
        self.xaml_variable = xaml_variable
        self.__get_name()
        self.__get_type()      


class Argument(Variable):

    datatype = ''
    name = ''
    direction = ''
    default_value = ''
    
    xaml_argument = None

    def __get_direction(self):
        d = self.xaml_argument.attrib['Type']
        if 'InOut' in d:
            d = 'InOut'
        elif 'In' in d:
            d = 'In'
        elif 'Out' in d:
            d = 'Out'
        else:
            raise 'Unrecognised argument direction'
        self.direction = d
    
    def __get_name(self):
        self.name = self.xaml_argument.attrib['Name']
    
    def __get_datatype(self):
        t = self.xaml_argument.attrib['Type']
        p = '\(x:(\w+)\)'
        reg = re.compile(p)
        r = reg.search(t)
        t = r.group(1)
        self.datatype = t

    def __init__(self, xaml_argument):
        self.xaml_argument = xaml_argument
        self.__get_name()
        self.__get_direction()
        self.__get_datatype()
        


class Activity():
    
    name = ''
    selector = ''
    activity_type = ''
    
    xaml_activity = None
    
    def __init__(self, xaml_activity):
        self.xaml_activity = xaml_activity
        self.name = self.__get_name()
        self.activity_type = self.__get_type()
        self.__get_selector()
    
    def __get_name(self):
        return self.xaml_activity.attrib['DisplayName']
    
    def __get_type(self):
        self.activity_type = self.xaml_activity.find('./Target')
    
    def __get_selector(self):
        for elem in self.xaml_activity.iter():
            try:
                self.selector = elem.attrib['Selector']
                return
            except KeyError:
                pass

                    
class Workflow():
    
    activities = []
    name = ''
    path = ''
    directory = ''
    variables = []
    arguments = []
    root = None
    
    def __find_all_activities(self, root):
        for child in root:
            if 'http://schemas.uipath.com/workflow/activities' in child.tag:
                a = Activity(child)
                self.activities.append(a)
            else:
                self.__find_all_activities(child)
    
    def __find_arguments(self):
        for c in self.root.iter('{http://schemas.microsoft.com/winfx/2006/xaml}Property'):
            a = Argument(c)
            self.arguments.append(a)
        
    def __find_variables(self):
        for c in self.root.iter('{http://schemas.microsoft.com/netfx/2009/xaml/activities}Variable'):
            v = Variable(c)
            self.variables.append(v)

    def __init__(self, path_workflow):
        self.path = path_workflow
        self.directory, self.name = os.path.split(path_workflow)
        
        tree = ET.parse(self.path)
        self.root = tree.getroot()
        self.__find_all_activities(self.root)
        self.__find_arguments()
        self.__find_variables()


class Project():
    
    name = ''
    description = ''
    size = ''
    workflows = []
    
    def __init__(self):
        pass



if __name__ == '__main__':
    path_xaml = r'C:\Users\markb\Documents\UiPath\02_Zoom_DispatchPlayers_backup\Sequence.xaml'
    w = Workflow(path_xaml)
    print('=======================')
    for ww in w.activities:
#        print(ww.name, ww.selector)
        pass
