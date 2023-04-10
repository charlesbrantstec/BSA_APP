import win32com.client
import openpyxl

# Specify the path to the Quicken file you want to open
quicken_file_path = r"C:\Users\username\Documents\Quicken\example.qdf"

# Open the Quicken file and navigate to the Saved Reports & Graphs section
quicken = win32com.client.Dispatch("Quicken.QuickenApplication")
quicken.Visible = True
quicken.OpenFile(quicken_file_path)
quicken.DoMenuCommand("CmdMenuID_Report")
quicken.DoMenuCommand("CmdSubMenuID_ReportsAndGraphs")

# Navigate to the report you want to export
quicken.FindInList("Report Name")
quicken.DoCommand("CmdID_ReportFilter")

# Get the report data and format it for Excel
report = quicken.ActiveReport
data = report.Data
rows = []
for i in range(1, data.Rows.Count + 1):
    row = [data(i, j).Text for j in range(1, data.Columns.Count + 1)]
    rows.append(row)

# Create a new Excel workbook and populate it with the report data
workbook = openpyxl.Workbook()
worksheet = workbook.active
for row in rows:
    worksheet.append(row)

# Save the Excel file
workbook.save("quicken_report.xlsx")

# Close Quicken
quicken.Quit()
