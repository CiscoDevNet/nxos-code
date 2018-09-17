import requests, urllib3

# Disable Self-Signed Cert warning for demo
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Assign requests.Session instance to session variable
session = requests.Session()

# Define URL and PAYLOAD variables
URL = "https://sbx-nxos-mgmt.cisco.com/api/aaaLogin.json"
PAYLOAD = {
          "aaaUser": {
            "attributes": {
              "name": "admin",
              "pwd": "Admin_1234!"
               }
            }
          }

# Obtain an authentication cookie
session.post(URL,json=PAYLOAD,verify=False)

# Define SYS_URL variable
SYS_URL = "http://sbx-nxos-mgmt.cisco.com/api/mo/sys.json"

# Obtain system information by making session.get call
# then convert it to JSON format then filter to system attributes
sys_info = session.get(SYS_URL,verify=False).json()

# Print raw data

print(sys_info)
