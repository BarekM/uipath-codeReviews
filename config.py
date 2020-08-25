import os


def create_dir(path_dir):
    if not(os.path.isdir(path_dir)):
        print('Creating directory: ' + path_dir)
        os.mkdir(path_dir)

blacklist_activities = ['ClickImage', 'ExcelApplicationScope']

default_activity_names = ['Click', 'Click Image', 'Type Into', 'While']

naming_convention = {
        'variables': '[a-z]+',
        'arguments': '[A-Z]+'
        }

path_reports = rf'{os.environ["HOMEPATH"]}\Documents\UiPathCodeReviews'
create_dir(path_reports)
