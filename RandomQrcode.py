# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 16:22:19 2018

@author: xiaowu
"""
import sys , os 
file_path=os.path.dirname(os.path.realpath(__file__))
sys.path.append(file_path)# get the path 
import pyqrcode,random
import adsk.core, adsk.fusion, traceback


global ui
app= None
ui= None

commandId='RandomQrcode'
commandName = 'Create RandomQrcode'
commandDescription = 'Create a Random height 3D qrcode in fusion'

handlers = []


class MyCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
          command = args.firingEvent.sender
          inputs = command.commandInputs
          

          
          qr = pyqrcode.create('U')
          #qr.png('famous-joke.png', scale=5)
          list01=qr.text()
          list01=list01.replace("\n","")  #handing the line break
          chara=inputs.itemById('string_input').value
          qr = pyqrcode.create(chara)
          list01=qr.text()
          list01=list01.replace("\n","")  #handing the line break
          size=inputs.itemById('Size_input').value
          n = len(list01)**0.5 # number of pixels in a row 
          d = size / n # single pixel width 
          h=inputs.itemById('High_input').value
          ran=inputs.itemById('Random_input').value
          create(list01,n,d,size,h,ran)





          print(inputs.itemById('Size_input').value)        
  

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def create(list01,n,d,size,h,ran):
  ui=None
  try:
      ran
      app = adsk.core.Application.get()
      ui = app.userInterface
      #doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
      design = app.activeProduct
      # Get the root component of the active design.
      rootComp = design.rootComponent
      # Create a new sketch on the xy plane.
      sketches = rootComp.sketches
      xyPlane = rootComp.xYConstructionPlane
      sketch = sketches.add(xyPlane)
      #define line cmd
      lines = sketch.sketchCurves.sketchLines      
      p0=adsk.core.Point3D.create(-d/2,-d/2,0)
      O_point=adsk.core.Point3D.create(size/2,size/2,0)
      C_point=adsk.core.Point3D.create(size,size,0)
      based = lines.addCenterPointRectangle(O_point, C_point)
      prof =sketch.profiles.item(0)
      thickness=size/25
      distance = adsk.core.ValueInput.createByReal(-thickness)
      ran=ran*10      
      #define extrude cmd
      extrudes = rootComp.features.extrudeFeatures      
      #create the model Base
      ext = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)     
      for x in range(len(list01)):
        if list01[x] == '1':         
          E_sketch=sketches.add(xyPlane)
          E_lines = E_sketch.sketchCurves.sketchLines
          px= (x // n)*d
          py= (x  % n)*d
          p=adsk.core.Point3D.create(px+d/2,py+d/2,0)
          p_corner = adsk.core.Point3D.create(px+d,py+d)
          pixel = E_lines.addCenterPointRectangle(p, p_corner)
          pixels = E_sketch.profiles.item(0)
          dh=h+(random.randint(0,ran))/10 
          P_distance = adsk.core.ValueInput.createByReal(dh)     
          P_ext = extrudes.addSimple(pixels,P_distance, adsk.fusion.FeatureOperations.JoinFeatureOperation)
  except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # When the command is done, terminate the script
            # This will release all globals which will remove all event handlers      

            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmd = args.command
            
            onExecute = MyCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)
            
            onDestroy = MyCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            # Keep the handler referenced beyond this function
            handlers.append(onDestroy)
            inputs = cmd.commandInputs
            global commandId
            

            inputs.addStringValueInput('string_input', 'character', 'Whats you want convert')
            inputs.addValueInput('Size_input', 'Size', 'cm', adsk.core.ValueInput.createByReal(5.0))
            inputs.addValueInput('High_input', 'Height', 'cm', adsk.core.ValueInput.createByReal(2.0))
            inputs.addValueInput('Random_input', 'Random', 'cm', adsk.core.ValueInput.createByReal(0.5))



          
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
    ui = None
    try:
        global app
        app = adsk.core.Application.get()
        ui = app.userInterface

        global commandId
        global commandName
        global commandDescription
        
        # Create command defintion
        cmdDef = ui.commandDefinitions.itemById(commandId)
        if not cmdDef:
            cmdDef = ui.commandDefinitions.addButtonDefinition(commandId, commandName, commandDescription)
            
        # Add command created event
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        # Keep the handler referenced beyond this function
        handlers.append(onCommandCreated)

        # Execute command
        cmdDef.execute()            

        # Prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))  
