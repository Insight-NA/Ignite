import json
import os
import sys
import dearpygui.dearpygui as dpg
import requests


numberOfHeaders = 1
numberOfParams = 1
headerItems = {}
paramItems = {}

savedRequests = {}
savedRequestsNames = []
sentRequestsResults = {}

windowPositionsFile = "window_positions.json"
font_path = os.path.join(os.path.dirname(__file__), 'Resources', 'Roboto-Black.ttf')
image_path = os.path.join(os.path.dirname(__file__), 'Resources', 'Insight_2024 Desktop Background_V1.jpg')

def get_request_names():
    """
    Populate the list of saved request names from the saved requests dictionary.
    """
    savedRequestsNames.clear()

    for key in list(savedRequests.keys()):
        savedRequestsNames.append(key)

dir_path = os.path.dirname(sys.executable)
if(os.path.exists(dir_path + '/savedRequests.txt')):
    with open(dir_path + '/savedRequests.txt') as f: 
        data = f.read()     
    savedRequests = json.loads(data) 
    get_request_names()

def update_request_call(sender, app_data):
    """
    Update the request call based on saved request data.
    """
    dpg.set_value("URL", savedRequests[app_data]["URL"])
    dpg.set_value("Type", savedRequests[app_data]["Type"])
    dpg.set_value("Body", savedRequests[app_data]["Body"])

    # Delete old headers and reset values
    global headerItems
    for header_key in headerItems.keys():
        dpg.delete_item(header_key)
    headerItems = {}
    global numberOfHeaders
    numberOfHeaders = 1

    # Add headers from the saved request to the GUI
    for header in savedRequests[app_data]["Headers"]:
        user_data = ["header_table", list(header.keys())[0], header[list(header.keys())[0]]]
        add_header(None, None, user_data)

    # Delete old params and reset values
    global paramItems
    for param_key in paramItems.keys():
        dpg.delete_item(param_key)
    paramItems = {}
    global numberOfParams
    numberOfParams = 1

    # Add headers from the saved request to the GUI
    for param in savedRequests[app_data]["Params"]:
        user_data = ["param_table", list(param.keys())[0], param[list(param.keys())[0]]]
        add_param(None, None, user_data)
        
def update_result(sender, app_data):
    """
    Update the result fields in the GUI based on the selected request result.
    """
    dpg.set_value("Status", sentRequestsResults[app_data]["Status"])
    dpg.set_value("Content", sentRequestsResults[app_data]["Content"])
    dpg.set_value("RequestType", sentRequestsResults[app_data]["RequestType"])
    dpg.set_value("RequestURL", sentRequestsResults[app_data]["RequestURL"])


def cancel_save():
    """
    Cancel the save operation and close the save window.
    """
    dpg.delete_item("saveWindow")


def get_number_of_headers():
    """
    Get the current number of headers.
    """
    return numberOfHeaders

def set_number_of_headers(new_value):
    """
    Set a new value for the number of headers.
    """
    global numberOfHeaders
    numberOfHeaders = new_value

def get_number_of_params():
    """
    Get the current number of parameters.
    """
    return numberOfParams

def set_number_of_params(new_value):
    """
    Set a new value for the number of parameters.
    """
    global numberOfParams
    numberOfParams = new_value


def save_request_to_file():
    """
    Save the current request to the saved requests file.
    """
    if dpg.get_value("SaveName") in savedRequestsNames:
        with dpg.popup(dpg.last_item()):
            dpg.add_text("A popup")
    else:
        headers = []
        for key in headerItems.keys():
            header_item = {
                dpg.get_value(headerItems[key]["HeaderTag"]): dpg.get_value(headerItems[key]["ValueTag"])
            }
            headers.append(header_item)
        params = []
        for key in paramItems.keys():
            param_item = {
                dpg.get_value(paramItems[key]["ParamTag"]): dpg.get_value(paramItems[key]["ValueTag"])
            }
            params.append(param_item)
        
        request_details = {
            "URL": dpg.get_value("URL"),
            "Auth": dpg.get_value("URL"),
            "Type": dpg.get_value("Type"),
            "Body": dpg.get_value("Body"),
            "Headers": headers,
            "Params": params,
        }

        global savedRequests
        savedRequests[dpg.get_value("SaveName")] = request_details
        dpg.delete_item("saveWindow")

        with open(os.path.join(dir_path, 'savedRequests.txt'), 'w+') as f:
            f.write(json.dumps(savedRequests))

        with open(os.path.join(dir_path, 'savedRequests.txt')) as f:
            data = f.read()
        
        savedRequests = json.loads(data)
        get_request_names()
        dpg.configure_item("savedRequestsList", items=savedRequestsNames)


def save_request():
    """
    Open a window to save the current request.
    """
    with dpg.window(width=250, height=150, pos=(400, 300), label="Request", no_close=True, tag="saveWindow"):
        dpg.add_input_text(hint="Request Name", tag="SaveName")
        dpg.add_button(label="Save", callback=save_request_to_file)
        dpg.add_button(label="Cancel", callback=cancel_save)

def add_header(sender, app_data, user_data):
    """
    Add a new header row to the headers table.
    """
    header_index = str(get_number_of_headers())
    
    with dpg.table_row(parent=user_data[0], tag="header" + header_index):
        dpg.add_input_text(hint="Key", tag="Header" + header_index + "Key", default_value=user_data[1])
        dpg.add_input_text(hint="Value", tag="Header" + header_index + "Value", default_value=user_data[2])
        dpg.add_button(label="X", width=50, callback=delete_header, user_data="header" + header_index)

    headerItems["header" + header_index] = {
        "HeaderTag": "Header" + header_index + "Key",
        "ValueTag": "Header" + header_index + "Value"
    }
    
    set_number_of_headers(get_number_of_headers() + 1)

def add_param(sender, app_data, user_data):
    """
    Add a new parameter row to the parameter table.
    """
    param_index = str(get_number_of_params())
    
    with dpg.table_row(parent=user_data[0], tag="param" + param_index):
        dpg.add_input_text(hint="Key", tag="Param" + param_index + "Key", default_value=user_data[1])
        dpg.add_input_text(hint="Value", tag="Param" + param_index + "Value", default_value=user_data[2])
        dpg.add_button(label="X", width=50, callback=delete_param, user_data="param" + param_index)

    paramItems["param" + param_index] = {
        "ParamTag": "Param" + param_index + "Key",
        "ValueTag": "Param" + param_index + "Value"
    }
    
    set_number_of_params(get_number_of_params() + 1)

def delete_header(sender, app_data, user_data):
    """
    Delete a header row from the headers table.
    """
    del headerItems[user_data]
    dpg.delete_item(user_data)

def delete_param(sender, app_data, user_data):
    """
    Delete a param row from the params table.
    """
    del paramItems[user_data]
    dpg.delete_item(user_data)

def send_request():
    """
    Send an HTTP request based on the current settings and update the GUI with the response.
    """
    dpg.set_value("Status", "")
    dpg.set_value("Content", "")
    dpg.set_value("RequestType", "")

    request_type = dpg.get_value("Type")
    url = dpg.get_value("URL")
    body = dpg.get_value("Body")
    auth_type = dpg.get_value("AuthType")
    auth = dpg.get_value("auth")

    payload = json.dumps(json.loads(body))

    headers = {
        'Content-Type': 'application/json',
    }
    for key in headerItems.keys():
        headers[dpg.get_value(headerItems[key]["HeaderTag"])] = dpg.get_value(headerItems[key]["ValueTag"])
        
    payload = {}
    for key in paramItems.keys():
        payload[dpg.get_value(paramItems[key]["ParamTag"])] = dpg.get_value(paramItems[key]["ValueTag"])
        
    

    if auth_type == "Bearer":
        headers['Authorization'] = f"{auth_type} {auth}"

    if(payload ==  {}): #If no params dont send the request
        response = requests.request(request_type, url, headers=headers, data=payload)
    else:
        response = requests.request(request_type, url, headers=headers, data=payload, params=payload)
        
        

    dpg.set_value("Status", response.status_code)
    dpg.set_value("RequestURL", url)
    dpg.set_value("RequestType", request_type)

    if response.status_code == 200:
        try:
            json_data = json.loads(response.text)
            pretty_json = json.dumps(json_data, indent=4)
        except:
            pretty_json = ""
        dpg.set_value("Content", pretty_json)
        result = {"Status": response.status_code, "Content": pretty_json, "RequestType" : request_type, "RequestURL" : url}
    else:
        result = {"Status": response.status_code, "Content": response.reason, "RequestType" : request_type, "RequestURL" : url}

    sentRequestsResults[str(len(sentRequestsResults))] = result

    dpg.configure_item("savedResultsList", items=list(sentRequestsResults.keys()))

def create_menu_bar():
    """
    Create the menu bar for the application viewport.
    """
    with dpg.viewport_menu_bar():
        with dpg.menu(label="Mode"):
            dpg.add_menu_item(label="Manual")
            dpg.add_menu_item(label="Automation")
            dpg.add_menu_item(label="Performance")
        
        with dpg.menu(label="FilePath"):
            dpg.add_menu_item(label="Set File Path")

        
# Create the DearPyGui context
dpg.create_context()

# Create the main viewport
dpg.create_viewport()
# create_menu_bar()
# Set up DearPyGui
dpg.setup_dearpygui()




# Load the image for the background
width, height, channels, data = dpg.load_image(image_path)
with dpg.texture_registry():
    texture_id = dpg.add_static_texture(width, height, data, tag="image_id")

# Load the font
with dpg.font_registry():
    default_font = dpg.add_font(font_path, 16)


# Create the main API window
with dpg.window(width=1600, height=900, label="API", no_close=True, no_bring_to_front_on_focus=True, tag="Window"):
    with dpg.drawlist(tag="drawlist", width=200, height=200, parent="Window"):
        # Get the size of the window
        height, width = dpg.get_item_rect_size("Window")
        # Draw the background image
        dpg.draw_image("image_id", (0, 0), (height, width), uv_min=(0, 0), uv_max=(1, 1))


# Create the Request window
with dpg.window(width=600, height=500, label="Request", no_close=True):
    # Bind the default font to the window
    dpg.bind_font(default_font)
    
    # Authorization section
    with dpg.collapsing_header(label="Authorization", default_open=True):
        with dpg.group(horizontal=True):
            dpg.add_combo(items=["None", "Bearer"], width=150, tag="AuthType", default_value="Bearer")
            dpg.add_input_text(hint="token", tag="auth")
    
    # Headers section
    with dpg.collapsing_header(label="Headers", default_open=True):
        with dpg.table(tag="header_table") as header_table:
            dpg.add_table_column(label="Key")
            dpg.add_table_column(label="Value")
            dpg.add_table_column(label="Delete")
        dpg.add_button(label="Add New Header", callback=add_header, user_data=["header_table", "", ""])
        
    with dpg.collapsing_header(label="Params", default_open=False):
        with dpg.table(tag="param_table") as param_table:
            dpg.add_table_column(label="Key")
            dpg.add_table_column(label="Value")
            dpg.add_table_column(label="Delete")
        dpg.add_button(label="Add New Param", callback=add_param, user_data=["param_table", "", ""])
    # Request section
    with dpg.collapsing_header(label="Request", default_open=True):
        dpg.add_text(default_value="URL")
        with dpg.group(horizontal=True):
            dpg.add_input_text(hint="google.com/test", tag="URL", default_value="https://")
            dpg.add_combo(items=["GET", "POST", "DELETE"], width=90, tag="Type", default_value="POST")
            sendRequest = dpg.add_button(label="Send", height=50, width=70, callback=send_request)
        dpg.add_text(default_value="Body")
        dpg.add_input_text(multiline=True, height=250, hint="{variable : test}", tag="Body", default_value={})

# Create the Results window
with dpg.window(label="Results", pos=(0, 520), width=275, height=225, no_close=True) as results_window:
    with dpg.group(horizontal=True):
        dpg.add_text(default_value="Request URL:")
        dpg.add_text(label="RequestURL", tag="RequestURL")
    with dpg.group(horizontal=True):
        dpg.add_text(default_value="Status Code:")
        dpg.add_text(label="Status", tag="Status")
    with dpg.group(horizontal=True):    
        dpg.add_text(default_value="Request Type:")
        dpg.add_text(label="RequestType", tag="RequestType")
    with dpg.group(horizontal=True):
        dpg.add_text(default_value="Content:")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="Content", multiline=True, readonly=True, width=-1, height=-1)

# Create the History window
with dpg.window(label="History", pos=(520, 520), width=275, height=225, no_close=True) as history_window:
    dpg.add_listbox(items=list(sentRequestsResults.keys()), width=200, tag="savedResultsList", callback=update_result)

# Create the Saved Requests window
with dpg.window(label="Saved Requests", pos=(700, 0), width=275, height=505, no_close=True) as saved_requests_window:
    dpg.add_listbox(items=savedRequestsNames, width=200, num_items=10, tag="savedRequestsList", callback=update_request_call)
    dpg.add_button(label="Save Current Request", callback=save_request)


def resize_img():
    """
    Resize the image to fit the window when the window size changes.
    """
    tsize = dpg.get_item_rect_size("Window")

    dpg.set_item_height("drawlist", tsize[1])
    dpg.set_item_width("drawlist", tsize[0])

    if dpg.does_alias_exist("drawlist"):
        dpg.delete_item("drawlist", children_only=True)
    
    dpg.draw_image("image_id", (0, 0), (tsize[0], tsize[1]), uv_min=(0, 0), uv_max=(1, 1), parent="drawlist")


with dpg.item_handler_registry(tag="window_handler"):
    dpg.add_item_resize_handler(callback=resize_img)

dpg.bind_item_handler_registry("Window", "window_handler")

# Create a theme for buttons
with dpg.theme() as item_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 180, 5), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

dpg.bind_item_theme(sendRequest, item_theme)

# Create a global theme for all items
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (78, 78, 78), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)

        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (45, 45, 48), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (58, 58, 60), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (93, 93, 94), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (129, 129, 131), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (76, 76, 77), category=dpg.mvThemeCat_Core)

        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6, category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)


# dpg.show_style_editor() #Show example code
dpg.show_viewport()
dpg.set_primary_window("Window", True)
dpg.start_dearpygui()
dpg.destroy_context()