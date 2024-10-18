# Import modules
import sqlite3
from nicegui import ElementFilter, app, ui, native
from nicegui.events import ValueChangeEventArguments
from typing import List, Tuple
# Import modules - END
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

# -
# -
# Variables for some functions in app

# Aibo API Path
BASE_PATH = 'https://public.api.aibo.com/v1'

connection = '1' # Connected status with cloud or app

aibo_daily_message = "Bleep bloop, I'm online!" # Aibo daily message under his image

dark_mode = ui.dark_mode(True) # Dark mode variable

aibo_image = "images/unitronix.png" # Aibo profile image

battery = "42%" # battery amount 

connection_type = "Wi-Fi" # connection type Wifi / Cloud

aibo_name = "Tom" # Aibo name

software_ver = "5.50" # Software version

mood = "Neutral" # Aibo Mood

# Variables - END 
# -
# -
# Top Menu Tabs

with ui.tabs().classes('w-full') as tabs:
    home = ui.tab('Main Page')
    controls = ui.tab('Controls')
    personalization = ui.tab('Personalization')
    settings = ui.tab('Settings')
    

# Top Menu Tabs - END
# -
# -
# -
# Tab Panels

with ui.tab_panels(tabs, value=personalization).classes('w-full'):
    # Home tab Module
    with ui.tab_panel(home):
        with ui.column():
            with ui.row().classes('w-4/4'):
                with ui.card().classes('w-2/4'):
                    # Main Grid - Welcome grid with app name
                    ui.label('Welcome to Aibo Toolkit').style('font-size: 200%; font-weight: 1000')
                    ui.label('Toolkit to manage your Aibo ERS 1000').style('font-size: 150%;')
                    # Main Grid - Welcome grid with app name - Updates timeline
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

                # ERS 1000 Stats
                with ui.card().classes('w-3/4'):
                    ui.chat_message(aibo_daily_message)
                    ui.image(aibo_image).classes('w-full')
                    
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
                            # -
                            # -
                            # -
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

        
        
           

        # Team loadout
        with ui.card():
            ui.label('Our Team:')

        with ui.row():
            with ui.card():
                with ui.image('images/apt.png').classes('w-20').props('fit=scale-down'):
                    ui.tooltip('AptitudeX').classes('bg-green')
                
            with ui.card():
                with ui.image('images/DoggiesGalore.png').classes('w-20').props('fit=scale-down'):
                    ui.tooltip('DoggiesGalore').classes('bg-green')

            with ui.card():
                with ui.image('images/ouija.png').classes('w-20').props('fit=scale-down'):
                    ui.tooltip('Ouija').classes('bg-green')
            
            with ui.card():
                with ui.image('images/unitronix.png').classes('w-20').props('fit=scale-down'):
                    ui.tooltip('UNITRONIX').classes('bg-green')

            with ui.card():
                with ui.image('images/sylva.png').classes('w-20').props('fit=scale-down'):
                    ui.tooltip('SylvaTheMoth').classes('bg-green')

            with ui.card():
                with ui.image('images/enfair.png').classes('w-20').props('fit=scale-down'):
                     ui.tooltip('Enfair Automata').classes('bg-green')

    with ui.tab_panel(controls):
                ui.label('Control Panel').style('font-size: 200%; font-weight: 1000')

    with ui.tab_panel(personalization):
                ui.label('Personalization Panel').style('font-size: 200%; font-weight: 1000')
    # -
    # -
    with ui.tab_panel(settings):
                ui.label('Settings Panel').style('font-size: 200%; font-weight: 1000')
                with ui.column():
                    ui.label('Add Aibo to app:')
                    with ui.dialog() as dialog, ui.card():
                        with ui.stepper().props('vertical').classes('w-full') as stepper:
                            with ui.step('Prepare Aibo'):
                                ui.label('Switch the network switch to position no.2')
                                ui.image('images/a_08.png').classes('w-80').props('fit=scale-down')
                                ui.label('Wait for the orange LED to light up')
                                with ui.stepper_navigation():
                                    ui.button('Next', on_click=stepper.next)
                            with ui.step('Finding Aibo via WIFI'):
                                ui.label('Mix the ingredients')
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
ui.run(title='AiboLabs Aibo Toolkit', reload=False, port=native.find_open_port())
