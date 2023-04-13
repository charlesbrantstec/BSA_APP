import win32com.client
import os

# Get the current working directory
cwd = os.getcwd()

# Create an instance of the Quicken application object
quicken = win32com.client.Dispatch("Quicken.Application.OFI")

# Open the Quicken data file
quicken_data_file = quicken.OpenFile("C:\\Users\\12158\\Downloads\\REIFAST CONSTRUCTION.QDF")

# Generate the report and set the report parameters
report_name = "Transactions by Category"
report = quicken_data_file.Reports.Item(report_name)
report.SetParameter("Date Range", "Custom")
report.SetParameter("Custom From", "01/01/2022")
report.SetParameter("Custom To", "12/31/2022")
report.SetParameter("Categories", "Subcontractors")
report.SetParameter("Show Subtotal By", "Payee")
report.SetParameter("Sort Order", "Ascending")
report.CreateReport()

# Export the report to a CSV file in the current working directory
export_file_name = "Subcontractors_expenses_2022.csv"
export_file_path = os.path.join(cwd, export_file_name)
report.ExportToCSV(export_file_path)