import os


def create_dir(path_dir):
    if not(os.path.isdir(path_dir)):
        print('Creating directory: ' + path_dir)
        os.mkdir(path_dir)

blacklist_activities = ['ClickImage',
                        'WaitImageVanish',
                        'HoverImage',
                        'OnImageVanish',
                        'ImageFound',
                        'FindImageMatches',
                        'OnImageAppear',
                        'ClickImageTrigger',
                        'ExcelApplicationScope',
                        'GetOCRText',
                        'FindOCRText',
                        'HoverOCRText',
                        'ClickOCRText',
                        'OCRTextExists',
                        'Set To Clipboard',
                        'Get From Clipboard',
                        'Copy Selected Text']

default_activity_names = ['Click',
                          'Click Image',
                          'Type Into',
                          'While',
                          'Do While',
                          'Write Line',
                          'Log Message',
                          'For Each Row',
                          'Build Data Table',
                          'Add Data Row',
                          'Read Range',
                          'Write Range',
                          'Read Cell',
                          'Write Cell',
                          'Send Hotkey',
                          'Filter Data Table',
                          'Matches',
                          'Is Match',
                          'Try Catch',
                          'Send Outlook Mail Message',
                          'Read CSV',
                          'Write CSV',
                          'Append to CSV',
                          'If',
                          'Flow Decision',
                          'For Each',
                          'Retry Scope',
                          'Flowchart',
                          'Flow Switch',
                          'Switch',
                          'Add To Collection',
                          'Throw',
                          'Set To Clipboard',
                          'Get From Clipboard',
                          'Copy Selected Text',
                          'Element Exists'
                          ]

naming_convention = {
        'variables': '[a-z]+',
        'arguments': '[A-Z]+'
        }

path_reports = rf'{os.environ["HOMEPATH"]}\Documents\UiPathCodeReviews'
create_dir(path_reports)
