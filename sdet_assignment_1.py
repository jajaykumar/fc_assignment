'''
This script is developed to test the scenario, where all the users of a particular city should have more than the required percentage of the todos task completed.

Sample script flow is as follows:

Given User has the todo tasks
And User belongs to the city 'FanCode'
Then User Completed task percentage should be greater than '50'%
'''

import requests
import logging
logging.basicConfig(level=logging.INFO)

root_uri = "https://jsonplaceholder.typicode.com"
city_locators = {"Fancode":{"Latitude":[-40,5],"Longitude":[5,100]}}

def fetch_user_todos():
    '''
    This API Method can be used to fetch all todo task details of all users '/todos' endpoint
    :param : None
    :return : Dict data of all the todo task details
    '''
    try:
        uri = f"{root_uri}/todos"
        todo_resp = requests.get(uri)
        return todo_resp.json()

    except Exception as err:
        logging.error(f"Exception occured with error '{err}'")
        return False

def fetch_all_user_details():
    '''
    This API Method can be used to fetch all the user details from all cities using the '/users' endpoint
    :param : None
    :return : Dict data of all the user details
    '''
    try:
        uri = f"{root_uri}/users"
        user_details = requests.get(uri)
        return user_details.json()

    except Exception as err:
        logging.error(f"Exception occured with error '{err}'")
        return False

def fetch_city_specific_user_details(city_name="Fancode"):
    '''
    This method can be used to fetch the details of all the users belonging to the given city using the latitude and longitude coordinates
    :param city_name : Name of the city using which the details of the users will be filtered
    :return city_specific_user_details: Dict data of the details of all the users belonging to the given city
    '''
    try:
        all_user_details = fetch_all_user_details()

        latitude_range=city_locators[city_name]["Latitude"]
        longitude_range = city_locators[city_name]["Longitude"]

        city_specific_user_details = []
        global city_specific_user_names
        city_specific_user_names = {}

        for user_index,users in enumerate(all_user_details):
            user_lat_info = eval(users["address"]["geo"]["lat"])
            user_long_info = eval(users["address"]["geo"]["lng"])

            #Verifying the latitude and longitude coordinates of the given city using the predefined dictionary variable 'city_locators' having the mapping between city name and lat and long coordinate ranges
            user_condition_exp = user_lat_info>=latitude_range[0] and user_lat_info<=latitude_range[1] and user_long_info>=longitude_range[0] and user_long_info<=longitude_range[1]
            if user_condition_exp:
                logging.info(f"User '{users['name']}' is present in city '{city_name}'")
                city_specific_user_details.append(users)
                city_specific_user_names[users['name']] = users['id']

        logging.info(f"Total number of users present in the city '{city_name}' is '{len(city_specific_user_details)}' ")

        return city_specific_user_details

    except Exception as err:
        logging.error(f"Exception occured with error '{err}'")
        return False



def fetch_city_specific_user_todos(city_name):
    '''
    This method can be used to fetch the todo task details of all the users belonging to the given city
    :param city_name : Name of the city using which the details of the users will be filtered
    :return city_specific_user_todo_details : Dict data of all the todo tasks details of all the users belonging to the given city
    :return users_having_no_tasks : List of users having no tasks assigned to them
    '''
    try:
        #Fetching all the users present in the specific city
        total_city_users=fetch_city_specific_user_details(city_name)
        #Fetching todo tasks of all users
        all_users_todos = fetch_user_todos()

        city_specific_user_todo_details={}

        #Checking if any of the user of the specific city does not have any todo tasks
        users_having_no_tasks = []
        todo_userids = list(set([tasks["userId"] for tasks in all_users_todos]))
        users_having_no_tasks = [user_name for user_name,user_id in city_specific_user_names.items() if user_id not in todo_userids]
        logging.info(f"List of users from '{city_name}' city not having any tasks --> '{users_having_no_tasks}'")

        for users in total_city_users:
            if users['name'] in users_having_no_tasks:
                logging.warning(f"User {users['name']} is not having any task. Not obtaining the task details")
                continue

            #Storing all the todo details, completed todo details and incomplete todo details for the specific user of the required city
            city_specific_user_todo_details[users['name']]={'all_todos_details':[],'completed_todos_details':[],'incomplete_todos_details':[]}

            for todos in all_users_todos:
                if todos['userId']==users['id']:
                    city_specific_user_todo_details[users['name']]['all_todos_details'].append(todos['title'])
                    if todos["completed"]==True:
                        city_specific_user_todo_details[users['name']]['completed_todos_details'].append(todos['title'])
                    else:
                        city_specific_user_todo_details[users['name']]['incomplete_todos_details'].append(todos['title'])

        return city_specific_user_todo_details, users_having_no_tasks

    except Exception as err:
        logging.error(f"Exception occured with error '{err}'")
        return False, False


def validate_the_completion_requirement(city_name,expected_completion_percentage=50):
    '''
    This method can be used to verify if all the users of the given city are having more than the expected completion percentage of their todos task completed.
    :param city_name : Name of the city using which the details of the users will be filtered
    :param expected_completion_percentage : Mention the expected completion percentage of the total todos to be completed.
    :return None
    '''
    try:
        user_todo_details,users_having_no_tasks = fetch_city_specific_user_todos(city_name)
        users_having_tasks = list(set(list(city_specific_user_names.keys()))-set(users_having_no_tasks))

        users_todos_analysis = {}

        #Computing the numerical data for total tasks, completed tasks and task completion percentage for the users having tasks
        for users in users_having_tasks:
            total_tasks = len(user_todo_details[users]['all_todos_details'])
            completed_tasks = len(user_todo_details[users]['completed_todos_details'])
            completion_percentage = round((completed_tasks/total_tasks)*100,2)
            users_todos_analysis[users]={"Total Tasks":total_tasks,'Completed Tasks':completed_tasks, 'Task Completion Percentage':completion_percentage}

        logging.info(users_todos_analysis)
        target_completed_user_list = [users for users, todo_analysis in users_todos_analysis.items() if todo_analysis['Task Completion Percentage']>expected_completion_percentage]
        target_incomplete_user_list = list(set(users_having_tasks) - set(target_completed_user_list))

        logging.info(f"List of users who have successfully completed more than {expected_completion_percentage}% of their todos tasks from '{city_name}' city is --> '{target_completed_user_list}'")
        logging.info(f"{len(target_completed_user_list)} users successfully completed more than {expected_completion_percentage}% of their todos tasks from '{city_name}' city")

        if len(target_completed_user_list) == len(users_having_tasks):
            logging.info(f"Success: All the {len(list(city_specific_user_names.keys()))} users have successfully completed more than {expected_completion_percentage}% of their todos tasks from '{city_name}' city")
        else:
            logging.error(f"Few users could not complete more than {expected_completion_percentage}% of their tasks. The list of users who could not achieve their target is --> {target_incomplete_user_list}")
            incomplete_task_detail_list = [{'User':users,'Incomplete tasks':user_todo_details[users]['incomplete_todos_details']} for users in target_incomplete_user_list]
            logging.info("INCOMPLETE TASK DETAILS IS AS FOLLOWS :\n-----------------------------------------------------")
            logging.info(incomplete_task_detail_list)

    except Exception as err:
        logging.error(f"Exception occured with error '{err}'")

if __name__=="__main__":
    validate_the_completion_requirement("Fancode",50)



