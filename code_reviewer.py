import os


from analysis import AnalysisProject
from excel import ExcelHandler


class CodeReviewer():
    
    def __init__(self, path_project_json, path_report='report.xlsx'):
        self.analysis = AnalysisProject(path_project_json)
        self.excel = ExcelHandler(path_report)
    
    def __save_data(self, sheet_name, data):
        self.excel.save_data(sheet_name, data)
    
    def review(self):
        self.review_selectorless()
        self.review_project_data()
        self.review_blacklisted_activities()
        self.review_defaulted_activities()
        self.review_duplicated_activities()
        self.review_selectors()
        self.review_variables_naming()
        self.review_arguments_naming()
        self.review_activities()
        self.review_workflows()
        self.review_loops()
    
    def review_project_data(self):
        self.__save_data('ProjectInfo', self.analysis.project_data)
    
    def review_selectorless(self):
        rows = [['Workflow', 'ActivityName', 'ActivityType']]
        for an in self.analysis.analyzed_workflows:
            s = an.activities_wo_selectors
            if len(s) != 0:
                for a in s:
                    rows.append([an.workflow.name, a.name, a.activity_type])
        self.__save_data('Selectorless', rows)
    
    def review_blacklisted_activities(self):
        rows = [['Workflow', 'ActivityName', 'ActivityType']]
        for an in self.analysis.analyzed_workflows:
            s = an.blacklisted_activities
            if len(s) != 0:
                for a in s:
                    rows.append([an.workflow.name, a.name, a.activity_type])
        self.__save_data('BlacklistedActivities', rows)
    
    def review_defaulted_activities(self):
        rows = [['Workflow', 'ActivityName', 'ActivityType']]
        for an in self.analysis.analyzed_workflows:
            s = an.defaulted_activity_names
            if len(s) != 0:
                for a in s:
                    rows.append([an.workflow.name, a.name, a.activity_type])
        self.__save_data('DefaultedActivities', rows)
        
    def review_duplicated_activities(self):
        rows = [['Workflow', 'ActivityName', 'Count']]
        for an in self.analysis.analyzed_workflows:
            s = an.duplicated_activity_names
            if len(s) != 0:
                for k, v in s.items():
                    rows.append([an.workflow.name, k, v])
        self.__save_data('DuplicatedActivities', rows)

    def review_selectors(self):
        rows = [['Workflow', 'ActivityName', 'ActivityType', 'Selector']]
        for an in self.analysis.analyzed_workflows:
            s = an.selectors
            if len(s) != 0:
                for a in s:
                    rows.append([an.workflow.name, a.name, a.activity_type, a.selector])
        self.__save_data('Selectors', rows)
    
    def review_variables_naming(self):
        rows = [['Workflow', 'VariableName', 'DataType']]
        for an in self.analysis.analyzed_workflows:
            s = an.variables_wrong_convention
            if len(s) != 0:
                for v in s:
                    rows.append([an.workflow.name, v.name, v.datatype])
        self.__save_data('VariablesNaming', rows)
        
    def review_arguments_naming(self):
        rows = [['Workflow', 'ArgumentName', 'DataType', 'Direction']]
        for an in self.analysis.analyzed_workflows:
            s = an.arguments_wrong_convention
            if len(s) != 0:
                for v in s:
                    rows.append([an.workflow.name, v.name, v.datatype, v.direction])
        self.__save_data('ArgumentsNaming', rows)
    
    
    def review_activities(self):
        rows = [['Workflow', 'ActivityType', 'Count']]
        for an in self.analysis.analyzed_workflows:
            s = an.activity_freq
            if len(s) != 0:
                for k, v in s.items():
                    rows.append([an.workflow.name, k, v])
        self.__save_data('ActivitiesCount', rows)
    
    def review_workflows(self):
        rows = [['Workflow', 'Activities', 'Variables', 'Arguments']]
        for an in self.analysis.analyzed_workflows:
            rows.append([an.workflow.name, an.counter_activities, an.counter_variables, an.counter_arguments])
        self.__save_data('WorkflowsAnalysis', rows)
        
    def review_loops(self):
        rows = [['Workflow', 'Activity', 'ActivityType', 'ExitCondition']]
        for w in self.analysis.project.workflows:
            for l in w.loops:
                rows.append([w.name, l.name, l.activity_type, l.exit_condition])
        self.__save_data('Loops', rows)
    
if __name__ == '__main__':
    p = r'C:\Users\markb\Documents\projects\uipath-codeReview\data\project1\project.json'
    p = r'C:\Users\markb\Documents\UiPath\01_Zoom_CreateRooms\project.json'
    pr = r'report.xlsx'
    try:
        os.remove(pr)
    except:
        pass
    
    cr = CodeReviewer(p, pr)
    cr.review()
#    cr.review_selectorless()
#    cr.review_project_data()
#    cr.review_blacklisted_activities()
#    cr.review_defaulted_activities()
#    cr.review_duplicated_activities()
#    cr.review_selectors()
#    cr.review_variables_naming()
#    cr.review_arguments_naming()
#    cr.review_activities()
#    cr.review_workflows()
#    cr.review_loops()
