import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope of the access required by the script
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the credentials JSON file for the service account
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    {
        "type": "service_account",
        "project_id": "candlespreadsheet",
        "private_key_id": "6bd7798aa8e7523ca2119464298885bc2df36393",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC0GzzoRPP6dc8B\nxeSv1MZIRjwLyqOYGes3uopPcyrTb4ghT8gP5F0VmgP337irnvj9Csk4if7eypo3\nI011dyHNjonrya8pcpXGm6cjtYLpBdNvk3XpXJmY6Q5hPx+vxwD/phu7wdG8GgEJ\nHpgLwDqqdo4edZgz7QbI8hF+x4rxUFZ1Jkx0SwouSCYwSkHvpp3Ej+9OiqVi+GMz\ny+S8UGkKFCGMZ4u6tDVfFt17uOt8AdQZDRhuCx6JwIpZ13pRVerLGS8JA9pXe/sP\nSo544g13/nheREg6BPlbVB6xIHU6uwi1/6VUbPp6DW1mUvi7x0o83P7wEhAHOCBF\nm3mbWLjFAgMBAAECggEAAgmWE0PQu61gk9BnSqaJZdlzFzcO3Xw9k5K9HYFILVvX\nBo0ja/DBj+V1Xldn3vHDwNpLxMEMHdW11OcUkMgUYff+XeRUMUDrDNZu3IgXcGnd\nOk6rW+IoIqqLWWhvF8sKh2OvW7V4NrLXr9lWwIeWLChq38d9s5nohyAvwiwrGDbQ\n+JUaBQ44afKH6KnQsjh2fq20zVycZ42/7R/Vbn6cmO+eYo/fcL7sso2vIhNL/RYy\n/NH4ZgZnz1ZR5eFbry3Z9/cdJqXRj/U1HGjhhvM5GQSbLwJFkKexiPgP9ElWXrol\n2Z9Dh9zFNtnJz4ymrd5HhE3tC9wKFPiifrm0v7JxqQKBgQDc9S2wYIoqTSlTcaBZ\nvfi3H7MF6jo75ENg1jI1aJ9qekb/x1PJ/ja6EVnP7dW6K+mPxliCjhG+2bz2b+el\nt1Vclynbl1pxWkUcFS2vQPggEa9xZZbIuH56WYnUe0Vg04XEqttIQ1Qj+/5GFCmm\nLfDJ0opvDu5yc2CAHlBYXNNM4wKBgQDQq4HHKKdz0oELVVzjIpBiFGewZNXigWqN\nCKIZTOBtlfEr2pv2pU8IJ1uuLNeyKcgGgfkQsm+F+M0E1mD5OvdJoZQ00jkx3xfn\nLxRJrqZ/Z6H9K5kqj5focKM+j+50ljPYOuMMkX9rJ8KIw8qhomJf3J+Mjbue7bEH\nsuJyTbo8NwKBgQC4bXU7WPk6Ibmyyo7bGTP2NeFJuJ3uy7Jpq5+w8KjPSUzlxcxs\nN2IaoMzkP1I72NdUiGvsXQT21ethjzo9Ge+IHyxy+7wkDQLOU+cT9xikO97CudbH\npyb6nK3syw+3qBZpd2scwAYFGxq8B6xT5tiqvK+Lz1y77w3HIoZRmvlLnQKBgQCv\nab1q4i4CG08Ha/btqTyednDDw8BY7FnZvQwnIIz5EjbumpLJQCWzwQI85M1do+nW\nLqRk+NrvUDtoeZ6DZKJEb2PbE22pEtVRLi5r0jl8mG2AGYpkUNluOGHCUdQuhaWH\ne9kp05W9Smsp9Qz92ze/RgOJcAvsiftrcWESnWyU+QKBgBRqydNNmE4gA4DOiQoo\ndjERX7CuUEDD1zaq6MFqGrdRBwqI/ouN9a6bqmoUV+i5Xn5yAujEZEk+iUp6THAY\n04uBfyLyJuzxysUazWQUxPLH/98LZhObZWoY/znwKTJWm1zyTpJcmrVU8Mxp53R0\nlVzkiNoCUCmeEPXVfRP22bVj\n-----END PRIVATE KEY-----\n",
        "client_email": "serv-308@candlespreadsheet.iam.gserviceaccount.com",
        "client_id": "105408628881015188371",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/serv-308%40candlespreadsheet.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    },
    scope
)

# Authorize the client with the service account credentials
client = gspread.authorize(creds)

# Open the Google Sheet by name
spreadsheet = client.open("KataleyaOrders")

# Select the first sheet or use its name
sheet = spreadsheet.sheet1

# Data to be written
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "Los Angeles"]
]

# Write data starting from row 1, column 1
def append_to_sheet(lst):
    sheet.append_row(lst)
