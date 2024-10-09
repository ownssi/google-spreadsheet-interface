import argparse
import sys
from datetime import datetime
import gspread
import pyperclip
from oauth2client.service_account import ServiceAccountCredentials
##############################################################################################
# Use example 1 - When you want to check a user has been selected(received our request):
# python DMrecorder.py -check username
# Use example 2 - If you are in rush and want to be really lazy without pasting the user name you want to search:
# python DMrecorder.py -check p
# Use example 3 - If you want to record your request:
# python DMrecorder.py -u username_request_sent -m message_content
# Use example 4 - Again, I made this function because I'm desperately lazy guy who doesn't even want to paste message content in the terminal:
# python DMrecorder.py -u username_request_sent -m p
# Use example 5 - My lazyniess even exists on username field:
# python DMrecorder.py -u p -m Hi! this is Do you want to participate my interview?
##############################################################################################


parser = argparse.ArgumentParser(description='If you pass just "p" for argument, then the script will use content in the clipboard for the argument')
parser.add_argument('-check', type=str, help='Check whether this user has received a request')
parser.add_argument('-u', type=str, help='User name request being sent')
parser.add_argument('-m', type=str, help='Message content')
parser.add_argument('-edit', type=str, help='Edit response status.')
args = parser.parse_args()
clipboard_content = pyperclip.paste()

con1 = (args.check or args.u or args.m or args.edit) #At least argument prompted
con2 = (args.check and args.u and args.m and args.edit) # All argument prompted
con3 = (args.check and (args.u or args.m or args.edit)) #Arg "check" and any other argu is prompted
con4 = (args.edit and (args.check or args.u or args.m)) # Arg "edit" and any other argu is prompted
if not con1 or con2 or con3 or con4:
    print("Wrong Argument")
    sys.exit()
elif not args.check and not (args.u and args.m):
    print("Both arguments -u(Username) and -c(Message content) should be provided")
    sys.exit()
elif args.edit:
    arg_lst = str(args.edit).split(' ')
    user_name = clipboard_content if arg_lst[0] == 'p' else arg_lst[0]
    status_change = arg_lst[1]
    

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open('CS6470 Interview Request')
sheet = spreadsheet.sheet1

if args.check:
    data = sheet.get_all_records()
    if str(args.check) == 'p':
        current_username = clipboard_content
    else:
        current_username = str(args.check)

    flag = True
    for row in data:
        print(row)
        if current_username == row['Username']:
            flag = False
            print("The user has already been received the request")
    if flag:
        print("Good to go!")
        print(current_username)

elif not args.check and args.u and args.m:
    now = datetime.now()
    current_date = now.day
    current_month = now.month
##############################################################################################
########################### Name #############################################################
    YOUR_NAME = "Jacob"
##############################################################################################
##############################################################################################

    if str(args.u) == 'p':
        new_row = [clipboard_content, YOUR_NAME,f'{current_month}/{current_date}',str(args.m),'Waiting(DM)']
    elif str(args.m) == 'p':
        new_row = [str(args.u), YOUR_NAME,f'{current_month}/{current_date}',clipboard_content,'Waiting(DM)']
    else:
        new_row = [str(args.u), YOUR_NAME,f'{current_month}/{current_date}',str(args.m),'Waiting(DM)']
    sheet.append_row(new_row)
    print("New request recorded!")
