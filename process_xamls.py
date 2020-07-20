import xml.etree.ElementTree as ET


class Activity():
    
    name = ''
    selector = ''
    activity_type = ''
    xaml_activity = ''
    
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
                return self.selector
            except KeyError:
                pass

            
            
class Workflow():
    
    activities = []
    name = ''
    path = ''
    
    def __find_all_activities(self, root):
        for child in root:
            if 'http://schemas.uipath.com/workflow/activities' in child.tag:
                a = Activity(child)
                self.activities.append(a)
            else:
                self.__find_all_activities(child)
    
    def __init__(self, path):
        self.activities = []
        self.path = path
        self.name = path.split('\\')[-1]
        
        tree = ET.parse(self.path)
        root = tree.getroot()
        self.__find_all_activities(root)


if __name__ == '__main__':
    path_xaml = r'C:\Users\markb\Documents\UiPath\02_Zoom_DispatchPlayers_backup\Sequence.xaml'
    w = Workflow(path_xaml)
    print('=======================')
    for ww in w.activities:
        print(ww.name, ww.selector)
