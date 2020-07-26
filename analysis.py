import re


from process_xamls import Project
import config as cfg


class AnalysisWorkflow():
    
    def __init__(self, workflow):
        self.workflow = workflow
        self.count_activities_freq()
        self.count_activities()
        self.get_blacklisted_activities()
        self.count_arguments()
        self.count_variables()
        self.get_activities_wo_selectors()
        self.get_duplicated_activity_names()
        self.get_defaulted_activity_names()
        self.get_activities_w_selectors()
        self.compliance_naming_variables()
        self.compliance_naming_arguments()

    def compliance_naming_variables(self):
        lv = []
        p = cfg.naming_convention['variables']
        reg = re.compile(p)
        for v in self.workflow.variables:
            if not(reg.match(v.name)):
                lv.append(v)
        self.variables_wrong_convention = lv
        return lv
    
    def compliance_naming_arguments(self):
        la = []
        p = cfg.naming_convention['arguments']
        reg = re.compile(p)
        for a in self.workflow.arguments:
            if not(reg.match(a.name)):
                la.append(a)
        self.arguments_wrong_convention = la
        return la
    
    def get_activities_w_selectors(self):
        s = [a for a in self.workflow.activities if a.selector != '{x:Null}' and a.selector]
        self.selectors = s
        return s
    
    def get_activities_wo_selectors(self):
        awos = [a for a in self.workflow.activities if a.selector == '{x:Null}']
        self.activities_wo_selectors = awos
        return awos
    
    def __build_dict_counter(self, d, key):
        if key in d:
            d[key] += 1
        else:
            d[key] = 1
        return d
    
    def get_duplicated_activity_names(self):
        d = dict()
        for a in self.workflow.activities:
            d = self.__build_dict_counter(d, a.name)
        dd = dict()
        for k in d:
            if d[k] > 1:
                dd[k] = d[k]
        self.duplicated_activity_names = dd
        return dd
    
    def count_activities_freq(self):
        d = dict()
        for a in self.workflow.activities:
            d = self.__build_dict_counter(d, a.activity_type)
        self.activity_freq = d
        return d
    
    def count_activities(self):
        c = len(self.workflow.activities)
        self.counter_activities = c
        return c
    
    def count_variables(self):
        c = len(self.workflow.variables)
        self.counter_variables = c
        return c
    
    def count_arguments(self):
        c = len(self.workflow.arguments)
        self.counter_arguments = c
        return c
    
    def get_blacklisted_activities(self):
        bl = [a for a in self.workflow.activities 
                                       if a.activity_type in cfg.blacklist_activities]
        self.blacklisted_activities = bl
        return(bl)

    def get_defaulted_activity_names(self):
        dl = [a for a in self.workflow.activities 
                                       if a.name in cfg.default_activity_names]
        self.defaulted_activity_names = dl
        return dl


class AnalysisProject():
    
    def __init__(self, path_project_json):
        self.__read_project(path_project_json)
        self.analyzed_workflows = []
        self.__analyse_workflows()
        self.__read_project_data()
    
    def __read_project(self, path):
        self.project = Project(path)
    
    def __read_project_data(self):
        d = []
        d.append(['Name', self.project.name])
        d.append(['Description', self.project.description])
        d.append(['Size', self.project.size])
        d.append(['Workflows', len(self.project.workflows)])
        d.append(['Activities', self.project.counter_activities])
        self.project_data = d
    
    def __analyse_workflows(self):
        for w in self.project.workflows:
            self.analyzed_workflows.append(AnalysisWorkflow(w))


if __name__ == '__main__':
    path_proj = r'C:\Users\markb\Documents\projects\uipath-codeReview\data\project1\project.json'
    p = Project(path_proj)
    w = p.workflows[0]
    a = AnalysisWorkflow(w)

#    print(a.activity_freq)
#    print('args: ', a.counter_arguments)
#    print('vars: ', a.counter_variables)
#    print('act: ', a.counter_activities)
#    for b in (a.blacklisted_activities):
#        print(b.activity_type)
#    for c in a.activities_wo_selectors:
#        print('Nie ma selektora:', c.name)
#    for d, e in a.duplicated_activity_names.items():
#        print(d, e)
#    print(a.selectors)
#    for f in a.defaulted_activity_names:
#        print(f.name)\
    ap = AnalysisProject(path_proj)
#    for bl in ap.analyzed_workflows:
#        for bbl in bl.blacklisted_activities:
#            print(bbl.name)