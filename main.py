# Import modules
import mysql.connector
from nicegui import ElementFilter, app, ui
from nicegui.events import ValueChangeEventArguments
# Import modules - END
# -
# -
# -
# Variables
dark_mode = ui.dark_mode(True)
# Variables - END
# -
# -
# Top Menu Tabs

with ui.tabs().classes('w-full') as tabs:
    home = ui.tab('Main Page')
    personalization = ui.tab('Personalization')
    settings = ui.tab('Settings')

# Top Menu Tabs - END
# -
# -
# -

with ui.tab_panels(tabs, value=personalization).classes('w-full'):
    with ui.tab_panel(home):
        
        with ui.column():
            with ui.row():
                with ui.card():
                    ui.label('Welcome to Aibo Toolkit').style('font-size: 200%; font-weight: 1000')
                    ui.label('Toolkit to manage your Aibo ERS 1000').style('font-size: 150%;')
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

                # ERS 1000 Stats
                with ui.card():
                    ui.image('images/a_03.png').classes('w-64').props('fit=scale-down')
                    with ui.card():
                        with ui.grid(columns=2):
                            ui.label('Connected').style('font-weight: 1000; color: green')
                            ui.label('')

                            ui.label('Connection type:').style('font-weight: 1000')
                            ui.label('WI-FI')

                            ui.label('Name:').style('font-weight: 1000')
                            ui.label('Tom')

                            ui.label('Battery:').style('font-weight: 1000')
                            ui.label('42%')

                            ui.label('Software:').style('font-weight: 1000')
                            ui.label('5.50')

            with ui.card():
                ui.label('Check Updates:').style('font-weight: 1000; font-size: 120%')
                with ui.row():
                     ui.icon('task_alt', color='green').classes('text-5xl')
                     with ui.list().props('dense separator'):
                        ui.item('You are using the latest version of the software').style('font-weight: 1000')
                        ui.item('Firmware version: 5.50 MOD')
                        ui.item('App version: 0.8')

        
        
           

        # Team loadout
        with ui.card():
            ui.label('Our Team:')

        with ui.row():
            with ui.card():
                ui.image('images/apt.png').classes('w-20').props('fit=scale-down')
                
            with ui.card():
                ui.image('images/DoggiesGalore.png').classes('w-20').props('fit=scale-down')

            with ui.card():
                ui.image('images/ouija.png').classes('w-20').props('fit=scale-down')
            
            with ui.card():
                ui.image('images/unitronix.png').classes('w-20').props('fit=scale-down')

            with ui.card():
                ui.image('images/sylva.png').classes('w-20').props('fit=scale-down')

    with ui.tab_panel(personalization):
                ui.label('Personalization Panel').style('font-size: 200%; font-weight: 1000')
    
    with ui.tab_panel(settings):
                ui.label('Settings Panel').style('font-size: 200%; font-weight: 1000')
                
                with ui.card():
                    
                    ui.label('Dark Mode:')
                    ui.switch('Dark mode').bind_value(dark_mode)


        
#Interface runing command
ui.run(title='AiboLabs Aibo Toolkit')