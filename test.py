#import openpyxl
#
#
#p = r'C:\Users\markb\Documents\projects\uipath-codeReview\tests\test11.xlsx'
#
#wb = openpyxl.load_workbook(p)
##wb = openpyxl.Workbook()
#
#
#ws = wb.active
#
#for row in range(1,10):
#    ws.append(['a', 'b'])
##    ws.append(range(20))
##    ws.append([1, 2, 3])
##    ws.append((1, 2, 3, 4))
#    
#
#
#print(wb.sheetnames)
#del wb['Sheet']
#print(wb.sheetnames)
#
#
#
#wb.save(p)
#

x = [1, 2, 3, 4]
y = [x, x, x]

z = [a
     for b in y
     for a in b]
print(len(z))