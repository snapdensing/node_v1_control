import gspread

gc = gspread.service_account(filename='./gsheets/gspread_credentials.json')

sh = gc.open_by_key('1CyLKDCl3noYfy95CFcEfl-R1kQ_MnxuK1gpcpCrXyVU')

worksheet = sh.worksheet('Status(testing)')


# Read test
val = worksheet.cell(2,1).value
print(val)

# Write test
newval = val + ',' + val
worksheet.update_cell(2,1,newval)
