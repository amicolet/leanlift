import logging
import shutil
import config
import getpartidsv2
import calendar
import time



# Configure logging
log_filename = r'C:\Users\16867789844979881303\Desktop\leanlift\Log Files/script_log.txt'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

current_GMT = time.gmtime()
time_stamp = str(calendar.timegm(current_GMT))

data = getpartidsv2.data

print('---Preparing Batch Request---')
logging.info('---Preparing Batch Request---')

batchliftqty = {
    "requests": []
}

batchrow = {
    "requests": []
}

for row in data:
    if 'stockID' in row:
        lift_request = {
            "_maCn": "ChangeRequest",
            "clientVersion": {
                "major": 2,
                "minor": 8,
                "patch": 1
            },
            "className": "Asset",
            "fields": "id, leanlift, dtmleanlift",
            "changeFields": "leanlift, dtmleanlift",
            "object": {
                "id": row['id'],
                "customFieldValues": {
                    "leanlift": int(row['Bestand']),
                    "dtmleanlift": getpartidsv2.refreshdate
                },
                "className": "Asset"
            }
        }
        batchliftqty['requests'].append(lift_request)

        if 'loadAsile' in row:
            row_request = {
                "_maCn": "ChangeRequest",
                "clientVersion": {
                    "major": 2,
                    "minor": 8,
                    "patch": 1
                },
                "className": "Stock",
                "fields": "id",
                "changeFields": "strRow",
                "object": {
                    "id": row['stockID'],
                    "strRow": row['Tablar'],
                    "className": "Stock"
                }
            }
            batchrow['requests'].append(row_request)


print("---Batch Request Ready---")
logging.info("---Batch Request Ready---")
print("---Executing Change Request for lean lift stock quantity---")
response = config.fiix.batch(batchliftqty)
print(response.json())
print("---Executing Change Request for lean lift rows---")
response = config.fiix.batch(batchrow)
print(response.json())
