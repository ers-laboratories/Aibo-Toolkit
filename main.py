# Import modules
import sqlite3
from nicegui import ElementFilter, app, ui, native, events
from typing import List, Tuple
from pathlib import Path
import random
import os
# Import modules - END
# -
# Create needed directory with database and for profile image

dir_1 = os.path.exists("bin") #Bin folder with database
dir_2 = os.path.exists("images/profile") #Folder will contain profile image for aibo

if not dir_1:
    os.makedirs("bin") #if folder doesn't exist, create him

if not dir_2:
     os.makedirs("images/profile") #if folder doesn't exist, create him
# -
# SQL Lite database configure

con = sqlite3.connect("bin/aibo_app.db")

cur = con.cursor()

# SQL Lite database table
sql = 'create table if not EXISTS settings (id int AUTO_INCREMENT PRIMARY KEY, aibo_image varchar(25), aibo_name varchar(25), aibo_software_ver varchar(25), aibo_mood varchar(25), aibo_deviceid varchar(255), aibo_access_token varchar(255), aibo_language varchar(10), aibo_eyes_color varchar(25), aibo_skin int, aibo_personality varchar(25));'
# Table - id, aibo_image (image name), aibo_name (Tom), aibo_software_ver (e.g 5.50), aibo_mood, aibo_deviceid, aibo_access_token, aibo_language (eng / jp), aibo_eyes_color (hash), aibo_skin (0-5), aibo_personality (name)
cur.execute(sql)

# Daily message list
daily_message_list = ["I'm up and running!","All systems are a go!","Ready to assist!","Percolating and pondering...","Percolating and pondering...","Just doing robot things.","Optimizing my processes.","Always learning, always growing.","Bleep bloop, I'm online!","I'm feeling a little rusty today.","Robot mode: activated!."]


# Variables for some functions in app

# Aibo API Path
aibo_api = 'https://public.api.aibo.com/v1'

connection = '1' # Connected status with cloud or app

aibo_daily_message = random.choice(daily_message_list) # Aibo daily message under his image

dark_mode = ui.dark_mode(True) # Dark mode variable

aibo_image = "images/profile/profile.png" # Aibo profile image

battery = "42%" # battery amount

connection_type = "Wi-Fi" # connection type Wifi / Cloud

aibo_name = "UNITRONIX" # Aibo name

software_ver = "5.50 (MOD 1.3.3)" # Software version

mood = "Neutral" # Aibo Mood

deviceid = ""

aibo_token = ""


# Top Menu Tabs

with ui.tabs().classes('w-full') as tabs:
    home = ui.tab('Main Page')
    controls = ui.tab('Controls')
    personalization = ui.tab('Personalization')
    service = ui.tab('Service / Repair')
    settings = ui.tab('Settings')
    

# Top Menu Tabs - END
# -
# -
# -
# Tab Panels

with ui.tab_panels(tabs, value=home).classes('w-full'):
    # Home tab Module
    with ui.tab_panel(home):
        ui.image('images/116.png').classes('absolute inset-0')

        with ui.row().classes('grid grid-cols-2 w-full'):
            with ui.card().classes('opacity-95 h-full'):
                # Main Grid - Welcome grid with app name
                ui.label('Welcome to Aibo Toolkit').style('font-size: 200%; font-weight: 1000')
                ui.label('Toolkit to manage your Aibo ERS 1000').style('font-size: 150%;')
                # Main Grid - Welcome grid with app name - Updates timeline
                with ui.scroll_area().style("width: 100%; height: 100%"):
                    with ui.timeline(side='right'):
                        ui.timeline_entry('Added support for changing Aibo eye color.',
                            title='Release of 0.8',
                            subtitle='May 18, 2024',
                            icon='rocket')
                        ui.timeline_entry('Added support for changing language.',
                            title='Release of 0.3',
                            subtitle='May 14, 2024'), 
                        ui.timeline_entry('Added support for AiboLabs Mod Software.',
                            title='Release of 0.1',
                            subtitle='May 14, 2024')
                        ui.timeline_entry(
                            title='Release of 0.01',
                            subtitle='May 14, 2024')
                        
                #Update card
                with ui.card().classes('w-full'):
                    ui.label('Check Updates:').style('font-weight: 1000; font-size: 120%')
                    with ui.row():
                        ui.icon('task_alt', color='green').classes('text-5xl')

                    with ui.list().props('dense separator'):
                                    ui.item('You are using the latest version of the software').style('font-weight: 1000')
                                    ui.item('Firmware version: 5.50 MOD')
                                    ui.item('App version: 0.8')

                    with ui.expansion('Release Notes', icon='work').classes('w-full'):
                                        ui.label('Stability update')
                                        ui.label('Security update')
                    ui.button('Check Updates', on_click=lambda: ui.notify('You are using the latest version of the software'))
                        
            # ERS 1000 Stats            
            with ui.card().classes('opacity-95'):
                    ui.label("Aibo stats:").style('font-size: 200%; font-weight: 1000')
                    ui.chat_message(aibo_daily_message)

                    #aibo image scaling
                    with ui.card().classes('w-full'):
                        ui.image(aibo_image).props('fit=scale-down').classes('rounded-full')

                    #aibo Vitals
                    with ui.card().classes('w-full'):
                        ui.label("Vitals:").style('font-size: 150%; font-weight: 1000')
                        with ui.row().classes('grid grid-cols-3 w-full'):
                            #Food
                            with ui.card().classes('w-full'):
                                with ui.knob(0.8, show_value=False, color='orange').classes('w-full h-full'):
                                    ui.icon('local_dining').classes('text-2xl')
                            #Water
                            with ui.card().classes('w-full'):
                                with ui.knob(0.5, show_value=False, color='blue').classes('w-full h-full'):
                                    ui.icon('water_drop').classes('text-2xl')
                            #Love
                            with ui.card().classes('w-full'):
                                with ui.knob(0.5, show_value=False, color='red').classes('w-full h-full'):
                                    ui.icon('favorite').classes('text-2xl')

                    with ui.dialog() as dialog, ui.card():
                        # Profile image upload and change
                        ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),
                        on_rejected=lambda: ui.notify('Rejected!'),
                        max_file_size=10_000_000).classes('max-w-full').props("accept=.png")
                        ui.button('Close', on_click=dialog.close)

                    ui.button('Change image', on_click=dialog.open)
                    with ui.card().classes('w-full'):
                        with ui.grid(columns=2):
                            #-
                            # Connection status checker - IF
                            if connection == '1':
                                ui.label('Connected').style('font-weight: 1000; color: green')
                                ui.label('')
                                
                            elif connection == '0':
                                ui.label('Disconnected').style('font-weight: 1000; color: red')
                                ui.label('')
                            # Connection type box
                            ui.label('Connection type:').style('font-weight: 1000')
                            ui.label(connection_type)
                            # -
                            # Aibo Name box
                            ui.label('Name:').style('font-weight: 1000')
                            ui.label(aibo_name)
                            # -
                            # Battery box
                            ui.label('Battery:').style('font-weight: 1000')
                            ui.label(battery)
                            # -
                            # Aibo software box
                            ui.label('Software:').style('font-weight: 1000')
                            ui.label(software_ver)

                            ui.label('Mood:').style('font-weight: 1000')
                            ui.label(mood)

                            ui.separator() # separator ui
                            ui.label()

                            ui.chip('Device ID', icon='content_copy', color='blue', on_click=lambda: ui.clipboard.write(deviceid))

                            ui.chip('Cloud Token', icon='content_copy', color='blue', on_click=lambda: ui.clipboard.write(aibo_token))
                            async def read() -> None:
                                ui.notify(await ui.clipboard.read())

            
        # Team loadout 
        with ui.card().classes("w-full opacity-95"):
            
            ui.label('Our Team:').style('font-weight: 1000')

            with ui.row().classes('grid grid-cols-8 gap-4 w-full'):
                with ui.card().classes('opacity-full'):
                    with ui.image('images/apt.png').props('fit=scale-down'):
                        ui.tooltip('AptitudeX').classes('bg-green').style('font-weight: 1000; font-size: 130%;')
                    
                with ui.card():
                    with ui.image('images/DoggiesGalore.png').props('fit=scale-down'):
                        ui.tooltip('DoggiesGalore').classes('bg-green').style('font-weight: 1000; font-size: 130%;')

                with ui.card():
                    with ui.image('images/ouija.png').props('fit=scale-down'):
                        ui.tooltip('Ouija').classes('bg-green').style('font-weight: 1000; font-size: 130%;')
                
                with ui.card():
                    with ui.image('images/unitronix.png').props('fit=scale-down'):
                        ui.tooltip('UNITRONIX').classes('bg-green').style('font-weight: 1000; font-size: 130%;')

                with ui.card():
                    with ui.image('images/sylva.png').props('fit=scale-down'):
                        ui.tooltip('SylvaTheMoth').classes('bg-green').style('font-weight: 1000; font-size: 130%;')

                with ui.card():
                    with ui.image('images/enfair.png').props('fit=scale-down'):
                        ui.tooltip('Enfair Automata').classes('bg-green').style('font-weight: 1000; font-size: 130%;')
                with ui.card():
                    with ui.image('images/ebi.png').props('fit=scale-down'):
                        ui.tooltip('Ebi (AiboWhisperer)').classes('bg-green').style('font-weight: 1000; font-size: 130%;')
                
                with ui.card():
                    with ui.image('images/virtual_paws.png').props('fit=scale-down'):
                        ui.tooltip('Virtual Paws').classes('bg-green').style('font-weight: 1000; font-size: 130%;')

    # Controls
    with ui.tab_panel(controls):
        ui.label('Control Panel').style('font-size: 200%; font-weight: 1000')

    # Personalization
    with ui.tab_panel(personalization):
        ui.image('images/116.png').classes('absolute inset-0')
        with ui.card().classes("w-full text-center"):
            ui.label('Personalize your AIBO :').style('font-size: 200%; font-weight: 1000')
        with ui.row().classes('grid grid-cols-2 w-full opacity-95'):

            #Aibo eye color picker
            with ui.card():
                ui.label("Eye color:").style('font-size: 150%; font-weight: 1000')
                with ui.row().classes('grid grid-cols-2 w-full'):
                    # color settings
                    with ui.card():
                        ui.label("Outer Color:")
                        with ui.button(icon='colorize') as outer_color:
                            ui.color_picker(on_pick=lambda e: outer_color.classes(f'!bg-[{e.color}]'))
                        ui.separator()
                        ui.label("inner Color:")
                        with ui.button(icon='colorize') as inner_color:
                            ui.color_picker(on_pick=lambda e: inner_color.classes(f'!bg-[{e.color}]'))
                        ui.separator()
                        ui.button('Save')
                    # eye overview
                    with ui.image("images/gui/eye.png").classes("w-25 h-25 rounded-full"):
                        with ui.card().classes("w-full h-full !bg-[#eeeee4] rounded-full") as outer_color:
                            with ui.card().classes("w-full h-full !bg-[#000000] rounded-full") as inner_color:
                                ui.label()
            

                        
    # Service
    with ui.tab_panel(service):
        ui.image('images/116.png').classes('absolute inset-0')
        with ui.card().classes("w-full text-center"):
            ui.label('Find Aibo Repair Service:').style('font-size: 200%; font-weight: 1000')
            #ebi card
        with ui.row().classes('grid grid-cols-3 w-full opacity-95'): 
            with ui.card():
                ui.label("Eberhard Ebi Suess").style('font-size: 200%; font-weight: 1000')
                ui.label("Europe: Germany").style('font-size: 130%; font-weight: 1000')
                ui.image("images/ebi.png").props('fit=scale-down').classes('full')
                with ui.card().classes('w-full'):
                    ui.label("Services offered:").style('font-weight: 1000')
                    with ui.list().props('dense separator'):
                        ui.item('1. Repair service for all Aibo Models')
                        ui.item('2. Customizing nearly all Aibo models')
                        ui.item('3. Battery service for all Aibo models')
                        ui.item('4. Selling used and refurbished Aibos')
                        ui.item('5. Answering technical questions about Aibos')

                        with ui.card().classes('w-full'):
                            # Facebook
                            ui.chip('Facebook', icon='bookmark', color='blue', on_click=lambda: ui.navigate.to("https://www.facebook.com/groups/977201906612506/user/1489153663/", new_tab=True)).classes("w-1/2")
                            # -
                            ui.chip('FB Group', icon='bookmark', color='blue', on_click=lambda: ui.navigate.to("https://www.facebook.com/groups/977201906612506", new_tab=True)).classes("w-1/2")
                                    
                     
    # Settings
    with ui.tab_panel(settings):
                ui.label('Settings Panel').style('font-size: 200%; font-weight: 1000')
                with ui.column():
                    ui.label('Add Aibo to app:')
                    with ui.dialog() as dialog, ui.card():
                        with ui.stepper().props('vertical').classes('w-full') as stepper:
                            with ui.step('Prepare Aibo'):
                                ui.label('Open lid from Aibo torso').style('font-size: 120%')
                                with ui.card().style("background-color: white").classes('w-full'):
                                    ui.image("images/tech/open_lid.png").classes('w-full')
                                ui.label('Switch the network switch to position no.2').style('font-size: 120%')
                                ui.label('See item no.2 in the picture').style('font-size: 120%')
                                with ui.card().style("background-color: white").classes('w-full'):
                                    ui.image("images/tech/wifi_con_1.png").classes('w-full')
                                ui.label('Wait for the orange LED to light up').style('font-size: 120%')
                                with ui.stepper_navigation():
                                    ui.button('Next', on_click=stepper.next)
                            with ui.step('Connecting Aibo to WI-FI network'):
                                ui.label('Enter your WI-FI network details:').style('font-size: 120%')
                                ui.input(label='SSDI:').style('font-size: 120%')
                                ui.input(label='Password:').style('font-size: 120%')
                                with ui.stepper_navigation():
                                    ui.button('Next', on_click=stepper.next)
                                    ui.button('Back', on_click=stepper.previous).props('flat')
                            with ui.step('Finish'):
                                ui.label('Bake for 20 minutes')
                                with ui.stepper_navigation():
                                    ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))
                                    ui.button('Back', on_click=stepper.previous).props('flat')



                    with ui.button('Add', on_click=dialog.open):
                        ui.tooltip('Configure Your Aibo to App').classes('bg-green')
                # -
                ui.separator() # separator ui
                # -
                with ui.switch('Dark mode ON/OFF').bind_value(dark_mode):
                    ui.tooltip('Enable dark mode').classes('bg-green')
                # -
                ui.separator() # separator ui 
                # -
                    

        
#Interface runing command
ui.run(title='AiboLabs Aibo Toolkit')
