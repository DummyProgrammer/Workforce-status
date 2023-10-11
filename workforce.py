import json
import requests
from datetime import datetime

# Define your Bearer token
token = "Bearer token here"

def main():

    print("Script started...")

    changeStatus = True
    while changeStatus:
        current_time_utc = datetime.utcnow()
        formatted_time_utc = current_time_utc.strftime('%H:%M:%S.%f')[:-3]  # Format to match time with microseconds

        # Shift schedule in workforce (UTC Timezone!)
        target_time = {'Start-up':'05:00:00.000',
                       'On-Queue':'06:29:00.000',
                       'Meal': '06:29:00.000',
                       'Break': '06:50:00.000',
                       'Case_Management': '13:00:00.000',
                       'End_Shift': '14:00:00.000'}
        
        # execution for status Busy -> Busy (start-up)
        if formatted_time_utc == target_time['Start-up']:
            expected = 'Busy'
            current = get_current_presence()
            if current != expected:
                print(f'Expected presence is {expected} but current status is {current}')
                patch_presence(expected)
                patched_presence = get_current_presence()
                print(f'Presence has been patched to {patched_presence}')
                print(f'User is now {get_current_presence()} -> Start-up')
            
            else:
                print('Presence is correct')

        # execution for status Break
        elif formatted_time_utc == target_time['Break']:
            expected = 'Break'
            current = get_current_presence()
            if current != expected:
                print(f'Expected presence is {expected} but current status is {current}')
                patch_presence(expected)
                patched_presence = get_current_presence()
                print(f'Presence has been patched to {patched_presence}')
                print(f'User is now {get_current_presence()}')
            
            else:
                print('Presence is correct')

        # execution for status Busy -> Case Management
        elif formatted_time_utc == target_time['Case_Management']:
            expected = 'Case_Management'
            current = get_current_presence()
            if current != expected:
                print(f'Expected presence is {expected} but current status is {current}')
                patch_presence(expected)
                patched_presence = get_current_presence()
                print(f'Presence has been patched to {patched_presence}')
                print(f'User is now {get_current_presence()} -> Case Management')

        # execution for status Meal
        elif formatted_time_utc == target_time['Meal']:
            expected = 'Meal'
            current = get_current_presence()
            if current != expected:
                print(f'Expected presence is {expected} but current status is {current}')
                patch_presence(expected)
                patched_presence = get_current_presence()
                print(f'Presence has been patched to {patched_presence}')
                print(f'User is now {get_current_presence()}')
            
            else:
                print('Presence is correct')
        
        #execution for when the shift end and script needs to be terminated
        elif formatted_time_utc == target_time['End_Shift']:
            print('Shift has ended.. Terminating script..')
            changeStatus = False  
        

def get_current_presence():
    userId = "2ff3c2af-f415-4cd3-b32c-7ce379049de1"  # user ID here
    region = "api.mypurecloud.com"                   # purecloud region
    resource = f"users/{userId}/presences/purecloud" 
    endpoint_uri = f"https://{region}/api/v2/{resource}"

   # Define the headers with the Bearer token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Make the POST request with headers
    try:
        response = requests.get(endpoint_uri, headers=headers)
    
        if response.status_code == 200:
            response_text = response.text
            dict_request = json.loads(response_text)
            current_presence = dict_request['presenceDefinition']['systemPresence']
            return current_presence
        else:
            print(f"Failed to patch status. Status code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")


def patch_presence(presence):
    userId = "2ff3c2af-f415-4cd3-b32c-7ce379049de1"  # user ID here
    region = "api.mypurecloud.com"                   # purecloud region
    resource = f"users/{userId}/presences/purecloud" 

    endpoint_uri = f"https://{region}/api/v2/{resource}"

   # Define the headers with the Bearer token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # get status request payload
    
    payload = get_status_request(presence)


    # Make the POST request with headers
    try:
        response = requests.patch(endpoint_uri, json=payload, headers=headers)
    
        if response.status_code == 200:
            print('Patching Success!')
        else:
            print(f"Failed to patch status. Status code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")


def get_status_request(presence):
    # status = Busy -> Busy
    if presence == 'Busy':
        return {
            "source": "PURECLOUD",
            "presenceDefinition": {
                "id": "1641d24f-be20-4ac6-9bf9-fa59e18d7200",
                "systemPresence": "Busy"
            }
        }
    # status = Busy -> Case Management
    if presence == 'Case_Management':
        return {
            "source": "PURECLOUD",
            "presenceDefinition": {
                "id": "690b9526-847d-4797-9d73-02d251f1ac38",
                "systemPresence": "Busy"
            }
        }

    # status = On Queue 
    if presence == "On_Queue":
        return {
            "source": "PURECLOUD",
            "presenceDefinition": {
                "id": "e08eaf1b-ee47-4fa9-a231-1200e284798f",
                "systemPresence": "On Queue"
            }
        }
    # status = Meal
    if presence == "Meal":
        return {
            "source": "PURECLOUD",
            "presenceDefinition": {
                "id": "3fd96123-badb-4f69-bc03-1b1ccc6d8014",
                "systemPresence": "Meal"
            }
        }
    # status = Break
    if presence == "Break":
        return {
            "source": "PURECLOUD",
            "presenceDefinition": {
                "id": "227b37e2-f1d0-4dd0-8f50-badd7cf6d158",
                "systemPresence": "Break"
            }
        }

main()