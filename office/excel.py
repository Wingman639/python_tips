
# -*- coding: utf-8 -*-
from win32com.client import Dispatch
import win32com.client
import time

xlRangeValueDefault = 10
xlRangeValueXMLSpreadsheet = 11
xlRangeValueMSPersistXML = 12

class easyExcel(object):
	"""A utility to make it easier to get at Excel.  Remembering
	to save the data is your problem, as is  error handling.
	Operates on one workbook at a time."""
	def __init__(self, filename=None):
		self.xlApp = win32com.client.Dispatch('Excel.Application')
		self.xlApp.Visible = 0
		if filename:
			self.filename = filename
			self.xlBook = self.xlApp.Workbooks.Open(filename)
		else:
			self.xlBook = self.xlApp.Workbooks.Add()
			self.filename = ''
	def __del__(self):
		self.close()
	def save(self, newfilename=None):
		if newfilename:
			self.filename = newfilename
			self.xlBook.SaveAs(newfilename)
		else:
			self.xlBook.Save()
	def close(self):
		self.xlBook.Close(SaveChanges=0)
		self.xlApp.Quit()
		del self.xlApp
		time.sleep(1) #give office center enough time to close, or next open will raise exception
	def getCell(self, sheet, row, col):
		"Get value of one cell"
		sht = self.xlBook.Worksheets(sheet)
		return sht.Cells(row, col).Value
	def setCell(self, sheet, row, col, value):
		"set value of one cell"
		sht = self.xlBook.Worksheets(sheet)
		sht.Cells(row, col).Value = value
	def getRange(self, sheet, row1, col1, row2, col2):
		"return a 2d array (i.e. tuple of tuples)"
		sht = self.xlBook.Worksheets(sheet)
		return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value
	def addPicture(self, sheet, pictureName, Left, Top, Width, Height):
		"Insert a picture in sheet"
		sht = self.xlBook.Worksheets(sheet)
		sht.Shapes.AddPicture(pictureName, 1, 1, Left, Top, Width, Height)
	def cpSheet(self, before):
		"copy sheet"
		shts = self.xlBook.Worksheets
		shts(1).Copy(None,shts(1))
	def getCellText(self, sheet, row, col):
		"Get text of one cell"
		sht = self.xlBook.Worksheets(sheet)
		return sht.Cells(row, col).Text



class ExcelHandler(easyExcel):
	def __init__(self, filename=None):
		easyExcel.__init__(self, filename)

	def sheetCount(self):
		return self.xlBook.Worksheets.Count

	def firstSheet(self):
		return self.xlBook.Worksheets(1)

	def sheetRowCount(self, sheet):
		return sheet.UsedRange.Rows.Count

	def sheetColCount(self, sheet):
		return sheet.UsedRange.Columns.Count

	def sheetToList(self, sheet):
		records = []
		for row in range(1, self.sheetRowCount(sheet) + 1 ):
			rowList = []
			for col in range(1, self.sheetColCount(sheet) + 1 ):
				rowList.append( sheet.Cells(row, col).Text )
			records.append( rowList )
		return records

	def sheetToDictRecords(self, sheet):
		def getRowDict(titles, rowList):
			rowDict = {}
			for i, part in enumerate(rowList):
				if len(titles) <= i: continue
				key = titles[i]
				value = rowList[i]
				rowDict[key] = value
			return rowDict

		data = self.sheetToList(sheet)
		if len(data) == 0: return []
		titles = data[0]
		records = []
		for row in range(1, len(data)):
			rowList = data[row]
			rowDict = getRowDict(titles, rowList)
			records.append(rowDict)
		return records


	def dataOf1stSheet(self):
		sht = self.firstSheet()
		return self.sheetToDictRecords(sht)

	def writeDataTo1stSheet(self, data):
		sheet = self.firstSheet()
		sheet.Columns("A:Z").NumberFormat = "@"
		self.writeDataToSheet(data, sheet)

	def writeDataToSheet(self, data, sheet):
		row = 1
		for record in data:
			self.writeRecordToSheetRow(record, sheet, row)
			row += 1

	def writeRecordToSheetRow(self, record, sheet, row):
		col = 1
		for item in record:
			sheet.Cells(row)
			sheet.Cells(row, col).Value = item
			col += 1

	def saveToFile(self, filePath, data):
		self.writeDataTo1stSheet(data)
		self.save(filePath)

if __name__ == "__main__":
	filePath = r'D:/workspace/Feature/O2/RAN3277/excel/WCDMA17_feature_list_INES_analysis.xlsx'

	def test_getCell():
		xls = easyExcel(filePath)
		print xls.getCell('Sheet1', 1, 2)

	def test_dataOf1stSheet():
		xls = ExcelHandler(filePath)
		print xls.dataOf1stSheet()


	def main():
		test_dataOf1stSheet()

	main()

