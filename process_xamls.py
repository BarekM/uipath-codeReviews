import os
import re
import json


import xml.etree.ElementTree as ET


class Variable():
    
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
#        self.datatype = ''
#        self.name = ''
#        self.scope = ''
#        self.default_value = ''
#        self.xaml_variable = None
        
        self.xaml_variable = xaml_variable
        self.__get_name()
        self.__get_type()      


class Argument(Variable):

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
    
    def __init__(self, xaml_activity):   
        self.xaml_activity = xaml_activity
        self.__get_name()
        self.__get_type()
        self.__get_selector()
        self.__check_if_loop()
    
    def __get_name(self):
        n = self.xaml_activity.attrib['DisplayName']
        self.name = n
    
    def __print_element(self, elem):
        print('===================')
        print('Tag: ', elem.tag)
        print('====')
#        for c in elem:
#            print(c.tag)
    
    def __get_type(self):
        p = '\}(\w+)'
        reg = re.compile(p)
        r = reg.search(self.xaml_activity.tag)
        t = r.group(1)
        t = t.replace('Interruptible', '')
        self.activity_type = t
    
    def __get_selector(self):
        for elem in self.xaml_activity.iter():
            try:
                self.selector = elem.attrib['Selector']
                return
            except KeyError:
                pass
        if not(hasattr(self, 'selector')):
            self.selector = None
    
    def __check_if_loop(self):
        if self.activity_type in ['While', 'DoWhile']:
            self.is_loop = True
            self.exit_condition = self.__get_loop_exit_condition()
        else:
            self.is_loop = False
            
    def __get_loop_exit_condition(self):
        for elem in self.xaml_activity.iter():
            try:
                return (elem.attrib['ExpressionText'])
            except:
                pass

                    
class Workflow():
    
    def __find_all_activities(self, root):
        for child in root:
            if 'http://schemas.uipath.com/workflow/activities' in child.tag:
                a = Activity(child)
                self.activities.append(a)
            else:
                self.__find_all_activities(child)
    
    def __find_arguments(self):
        self.arguments = []
        for c in self.root.iter('{http://schemas.microsoft.com/winfx/2006/xaml}Property'):
            a = Argument(c)
            self.arguments.append(a)
        
    def __find_variables(self):
        self.variables = []
        for c in self.root.iter('{http://schemas.microsoft.com/netfx/2009/xaml/activities}Variable'):
            v = Variable(c)
            self.variables.append(v)

    def get_loops(self):
        l = []
        for a in self.activities:
            if a.activity_type in ['While', 'DoWhile']:
                pass            
    
    def __init__(self, path_workflow):
        self.activities = []
        
        self.path = path_workflow
        self.directory, self.name = os.path.split(path_workflow)
        
        tree = ET.parse(self.path)
        self.root = tree.getroot()
        self.__find_all_activities(self.root)
        self.__find_arguments()
        self.__find_variables()


class Project():
    
    def __read_proj_json(self):
        with open (self.path_proj_json, 'r') as f:
            self.dict_proj_json = json.load(f)
    
    def __get_proj_name(self):
        self.name = self.dict_proj_json['name']
    
    def __get_proj_description(self):
        self.description = self.dict_proj_json['description']
    
    def __get_proj_size(self):
        total_size = 0
        for path, dirs, files in os.walk(self.path_proj_dir):
            for f in files:
                fp = os.path.join(path, f)
                total_size += os.path.getsize(fp)
        self.size = total_size
    
    def __get_all_xamls(self):
        xamls = []
        for p, d, f in os.walk(self.path_proj_dir):
            xamls += [os.path.join(p, x) for x in f if x.split('.')[-1].upper() == 'XAML']
        return xamls

    def __get_workflows(self):
        xamls = self.__get_all_xamls()
        self.workflows = [Workflow(w) for w in xamls]
    
    def __str__(self):
        return f'''Name: {self.name}; Description: {self.description}; Size: {self.size}; Workflows: {len(self.workflows)}'''
    
    def __init__(self, path_proj_json):
#        self.name = ''
#        self.description = ''
#        self.size = ''
#        self.workflows = []
#        self.path_proj_json = ''
#        self.path_proj_dir = ''
#        self.dict_proj_json = None
        
        self.path_proj_json = path_proj_json
        self.path_proj_dir, _ = os.path.split(path_proj_json)
        self.__read_proj_json()
        self.__get_proj_name()
        self.__get_proj_description()
        self.__get_proj_size()
        self.__get_workflows()
        



if __name__ == '__main__':
    p1 = r'C:\Users\markb\Documents\projects\uipath-codeReview\data\project1\Main.xaml'
    p2 = r'C:\Users\markb\Documents\projects\uipath-codeReview\data\project1\Sequence.xaml'
    
    w1 = Workflow(p1)
#    w2 = Workflow(p2)

    for a in w1.activities:
        if a.is_loop:
            print(a.activity_type, a.exit_condition)