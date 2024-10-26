# Import modules
import sqlite3
import random
import os
from fastapi import Request
from nicegui import ElementFilter, app, ui, native, events
from typing import List, Tuple
from pathlib import Path
from nicegui.elements import markdown

# Import modules - END

ui.query('.nicegui-content').classes('w-full')
ui.query('.q-page').classes('flex')
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
#cur.execute(sql)

# Daily message list and function
daily_message_list = ["I'm up and running!","All systems are a go!","Ready to assist!","Percolating and pondering...","Percolating and pondering...","Just doing robot things.","Optimizing my processes.","Always learning, always growing.","Bleep bloop, I'm online!","I'm feeling a little rusty today.","Robot mode: activated!."]

aibo_daily_message = random.choice(daily_message_list) # Aibo daily message under his image

# Variables for some functions in app

# mobile layout enable/disable

ml_settings = False

home_page_layout = 'grid grid-cols-2 w-full'
controls_layout = ''
personalization_layout = 'grid grid-cols-2 w-full opacity-95'
service_layout = 'grid grid-cols-3 w-full opacity-95'


def mobile_row_enable():
    home_row.default_classes('grid grid-cols-1 w-full')

# Aibo API Path
aibo_api = 'https://public.api.aibo.com/v1'

connection = '1' # Connected status with cloud or app

dark_mode = ui.dark_mode(True) # Dark mode variable

aibo_image = "images/profile/profile.png" # Aibo profile image

battery = "42%" # battery amount

connection_type = "Wi-Fi" # connection type Wifi / Cloud

aibo_name = "UNITRONIX" # Aibo name

software_ver = "5.50 (MOD 1.3.3)" # Software version

mood = "Neutral" # Aibo Mood

deviceid = "" # DeviceID

aibo_token = "" # Cloud Token

background_image_set = 'images/background/35.png' # Background image

aibo_coins = '3000' #Aibo Coins


# Top Menu Tabs

with ui.tabs().classes('w-full') as tabs:
    home = ui.tab('Main Page')
    controls = ui.tab('Controls')
    personalization = ui.tab('Personalization')
    playful_aibo = ui.tab('Playfull Aibo')
    service = ui.tab('Service / Repair')
    settings = ui.tab('Settings')


# Tab Panels
with ui.tab_panels(tabs, value=settings).classes('w-full'):
    # Home tab Module
    with ui.tab_panel(home):
        ui.image(background_image_set).classes('absolute inset-0')
        with ui.row().classes('grid grid-cols-2 w-full') as home_row:
            with ui.card().classes('opacity-95 h-full'):
                # Main Grid - Welcome grid with app name
                ui.label('Welcome to Aibo Toolkit').style('font-size: 200%; font-weight: 1000')
                ui.label('Toolkit to manage your Aibo ERS 1000').style('font-size: 150%;')
                # Main Grid - Welcome grid with app name - Updates timeline
                            
                #aibo coins and lvl
                with ui.row().classes('grid grid-cols-2 w-full'):

                    #aibo coins
                    with ui.card().classes('w-full h-full'):
                        ui.label('Aibo Coins:').style('font-weight: 1000; font-size: 120%')
                        with ui.row():
                            #aibo coins icon
                            ui.icon('paid', color='primary').classes('text-5xl')
                            #aibo coins amount with variable
                            ui.label(aibo_coins).style('font-weight: 1000; font-size: 230%')

                    #aibo lvl
                    with ui.card().classes('w-full h-full'):
                        ui.label('Aibo Level:').style('font-weight: 1000; font-size: 120%')
                        with ui.row().classes('grid grid-cols-1 w-full'):
                            #aibo coins icon
                            ui.label('Lvl: 1').style('font-weight: 1000; font-size: 120%')
                            #aibo coins amount with variable
                            ui.linear_progress()
                    

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
                    with ui.card().classes('w-full justify-center').style('text-align: center'):
                        ui.image(aibo_image).props('fit=scale-down').classes('rounded-full ').style('height: 50%; width: 50%; text-align: center')

                    with ui.dialog() as dialog, ui.card():
                        # Profile image upload and change 
                        ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),
                        on_rejected=lambda: ui.notify('Rejected!'),
                        max_file_size=10_000_000).classes('max-w-full').props("accept=.png")
                        ui.button('Close', on_click=dialog.close)
                    ui.button('Change image', on_click=dialog.open)

                    #aibo Vitals
                    with ui.card().classes('w-full'):
                        ui.label("Vitals:").style('font-size: 150%; font-weight: 1000')
                        with ui.row().classes('grid grid-cols-3 w-full'):
                            #Food
                            with ui.card().classes('w-full'):
                                with ui.circular_progress(value=0.3, show_value=False, color='orange').classes('w-full h-full items-center m-auto') as food_progress:
                                    ui.icon('local_dining', color='primary').classes('text-2xl').props('flat round').classes('w-full h-full')
                            #Water
                            with ui.card().classes('w-full'):
                                with ui.circular_progress(value=0.5, show_value=False, color='blue').classes('w-full h-full items-center m-auto') as water_progress:
                                    ui.icon('water_drop', color='primary').classes('text-2xl').props('flat round').classes('w-full h-full')
                            #Love
                            with ui.card().classes('w-full'):
                                with ui.circular_progress(value=0.8, show_value=False, color='red').classes('w-full h-full items-center m-auto') as love_progress:
                                    ui.icon('favorite', color='primary').classes('text-2xl').props('flat round').classes('w-full h-full')

                    

                    
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

        ui.image(background_image_set).classes('absolute inset-0')
        with ui.card().classes("w-full text-center"):
            ui.label('Personalize your AIBO :').style('font-size: 200%; font-weight: 1000')
        with ui.row().classes(personalization_layout):

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
            #language change
            with ui.card():
                ui.label("Language change:").style('font-size: 150%; font-weight: 1000')
                with ui.tabs().classes('w-full') as tabs:
                    ui.tab('h', label='English')
                    ui.tab('a', label='Japanese')
                with ui.tab_panels(tabs, value='h').classes('w-full'):
                    with ui.tab_panel('h'):
                        with ui.row().classes('grid grid-cols-2 w-full'):
                            ui.image("images/us.png").classes("rounded-full")
                            with ui.card():
                                ui.label('Global English for Aibo')
                                ui.button('Apply', on_click=lambda: ui.notify('English language applied to Aibo'))
                    with ui.tab_panel('a'):
                        with ui.row().classes('grid grid-cols-2 w-full'):
                            ui.image("images/jp.png").classes("rounded-full")
                            with ui.card():
                                ui.label('Global Japanese for Aibo')
                                ui.button('Apply', on_click=lambda: ui.notify('Japanese language applied to Aibo'))
    
    # Playful Aibo
    with ui.tab_panel(playful_aibo):
        ui.image(background_image_set).classes('absolute inset-0')
        with ui.row().classes('grid grid-cols-2 w-full') as home_row:
            #left card
            with ui.card().classes('opacity-95 h-full'):
                #aibo coins
                with ui.card().classes('w-full'):
                    ui.label('Aibo Coins:').style('font-weight: 1000; font-size: 120%')
                    
                    with ui.row():
                        #aibo coins icon
                        ui.icon('paid', color='primary').classes('text-5xl')
                        #aibo coins amount with variable
                        ui.label(aibo_coins).style('font-weight: 1000; font-size: 230%')

                #playful tab menu with shops        
                with ui.tabs().classes('w-full') as playful_tabs:
                    ui.tab('restaurant', label='Restaurant', icon='restaurant')
                    ui.tab('toy_shop', label='Toy Shop', icon='toys')

                with ui.tab_panels(playful_tabs, value='restaurant').classes('w-full'):
                    
                    with ui.tab_panel('restaurant').classes('h-full'):
                        
                        with ui.row().classes('grid grid-cols-1 w-full'):
                            with ui.scroll_area().classes('w-full'):
                                #Big Meal
                                with ui.card().classes('w-full').style('height: 100%'):
                                    with ui.row().classes('grid grid-cols-2 w-full'):
                                        ui.icon('fastfood', color='primary').classes('w-full h-full text-8xl')
                                        with ui.card():
                                            #Describe
                                            ui.label('Large Meal').style('font-weight: 1000; font-size: 120%')
                                            with ui.list().props('dense separator'):
                                                ui.item('Food: 100%')
                                                ui.item('Water: 100%')
                                                ui.item('Level: +10 points')
                                            ui.separator()
                                            ui.button('Buy').classes('w-full')

                                #Medium Meal
                                with ui.card().classes('w-full'):
                                    with ui.row().classes('grid grid-cols-2 w-full'):
                                        ui.icon('dinner_dining', color='primary').classes('w-full h-full text-8xl')
                                        with ui.card():
                                            #Describe
                                            ui.label('Medium Meal').style('font-weight: 1000; font-size: 120%')
                                            with ui.list().props('dense separator'):
                                                ui.item('Food: 50%')
                                                ui.item('Water: 50%')
                                                ui.item('Level: +5 points')
                                            ui.separator()
                                            ui.button('Buy').classes('w-full')

                    with ui.tab_panel('toy_shop'):
                        ui.label('Second tab')    

                        
            # ERS 1000 Stats            
            with ui.card().classes('opacity-95'):

                    #aibo image scaling
                    with ui.card().classes('w-full'):
                        ui.image(aibo_image).props('fit=scale-down').classes('rounded-full')

                    with ui.dialog() as dialog, ui.card():
                        # Profile image upload and change 
                        ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),
                        on_rejected=lambda: ui.notify('Rejected!'),
                        max_file_size=10_000_000).classes('max-w-full').props("accept=.png")
                        ui.button('Close', on_click=dialog.close)

                    #aibo Vitals
                    with ui.card().classes('w-full'):
                        ui.label("Vitals:").style('font-size: 150%; font-weight: 1000')
                        with ui.row().classes('grid grid-cols-3 w-full'):

                            #Food
                            with ui.card().classes('w-full'):
                                with ui.circular_progress(value=0.3, show_value=False, color='orange').classes('w-full h-full items-center m-auto') as food_progress:
                                    ui.button(icon='local_dining', on_click=lambda: food_progress.set_value(food_progress.value + 0.1)).props('flat round').classes('w-full h-full')
                            
                            #Water
                            with ui.card().classes('w-full'):
                                with ui.circular_progress(value=0.5, show_value=False, color='blue').classes('w-full h-full items-center m-auto') as water_progress:
                                    ui.button(icon='water_drop', on_click=lambda: water_progress.set_value(water_progress.value + 0.1)).props('flat round').classes('w-full h-full')
                            
                            #Love
                            with ui.card().classes('w-full'):
                                with ui.circular_progress(value=0.8, show_value=False, color='red').classes('w-full h-full items-center m-auto') as love_progress:
                                    ui.button(icon='favorite', on_click=lambda: love_progress.set_value(love_progress.value + 0.1)).props('flat round').classes('w-full h-full')

    # Service   
    with ui.tab_panel(service):
        ui.image(background_image_set).classes('absolute inset-0')
        with ui.card().classes("w-full text-center"):
            ui.label('Find Aibo Repair Service:').style('font-size: 200%; font-weight: 1000')
            #ebi card
        with ui.row().classes('grid grid-cols-2 w-full opacity-95'): 
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
                #Dark mode switch
                with ui.switch('Dark mode').bind_value(dark_mode) as dark_mode_switch:
                    ui.label('Dark Mode Enabled!').bind_visibility_from(dark_mode_switch, 'value').style('color: green')
                    ui.tooltip('Enable dark mode').classes('bg-green')

                ui.separator() # separator ui

                #Mobile layout switch
                with ui.switch('Mobile layout (comming soon)', value=False, on_change= lambda: ui.navigate.reload()) as mobile_layout_switch:
                    ui.label('Mobile interface is Enabled!').bind_visibility_from(mobile_layout_switch, 'value').style('color: green')
                    ui.tooltip('Enable mobile layout for smartphones').classes('bg-green')
                
                ui.separator()

                #GUI Primary color changer
                ui.label('GUI Primary color')
                with ui.button(icon='colorize'):
                    ui.color_picker(on_pick=lambda e: ui.colors(primary =f'{e.color}'))

                ui.separator() # separator ui


        
#Interface runing command
ui.run(title='AiboLabs Aibo Toolkit')
