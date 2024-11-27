--[[
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This Lua script is to implement Task 2B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
]]--


--[[
# Team ID:			[ NB_1972]
# Author List:		[ Neha Yadav, Rashmi Sarwal, Nisha, Harshita Pahwa]
# Filename:			task_2b
# Functions:        createWall, saveTexture, retrieveTexture, reapplyTexture, receiveData, generateHorizontalWalls, 
#                   generateVerticalWalls, deleteWalls, createMaze, sysCall_init, sysCall_beforeSimulation
#                   sysCall_afterSimulation, sysCall_cleanup, delobj, zip
# Global variables:	
# 					[ del_obj, maze_array ]
]]--

--[[
##################### GLOBAL VARIABLES #######################
## You can add global variables in this section according   ##
## to your requirement.                                     ##
## DO NOT TAMPER WITH THE ALREADY DEFINED GLOBAL VARIABLES. ##
##############################################################
]]--

del_obj = {}         --To Keep record of deleted walls when creating maze
maze_array = {}
baseHandle = -1       --Do not change or delete this variable
textureID = -1        --Do not change or delete this variable
textureData = -1       --Do not change or delete this variable

--############################################################

--[[
##################### HELPER FUNCTIONS #######################
## You can add helper functions in this section according   ##
## to your requirement.                                     ##
## DO NOT MODIFY OR CHANGE THE ALREADY DEFINED HELPER       ##
## FUNCTIONS                                                ##
##############################################################
]]--


--[ Function to delete wall ]--
function delobj(n)   
    res=sim.getObjectHandle(n) --To get wall handle
    result=sim.removeObject(res) --To remove wall
end

--[ To get individual element from Hor, Ver and index tables simultaneously later in createMaze() function ]--
function zip(...)
  local arrays, ans = {...}, {}
  local index = 0
  return
    function()
      index = index + 1
      for i,t in ipairs(arrays) do
        if type(t) == 'function' then ans[i] = t() else ans[i] = t[index] end
        if ans[i] == nil then return end
      end
      return unpack(ans)
    end
end
    
--[[
**************************************************************
	Function Name : createWall()
    Purpose:
	---
	Creates a black-colored wall of dimensions 90cm x 10cm x 10cm

	Input Arguments:
	---
	None
	
	Returns:
	---
	wallObjectHandle : number
    
    returns the object handle of the created wall
	
	Example call:
	---
	wallObjectHandle = createWall()
**************************************************************	
]]--
function createWall()
    wallObjectHandle = sim.createPureShape(0, 26, {0.09, 0.01, 0.1}, 0, nil)
    sim.setShapeColor(wallObjectHandle, nil, sim.colorcomponent_ambient_diffuse, {0, 0, 0})
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_collidable)
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_measurable)
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_detectable_all)
    sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_renderable)
    return wallObjectHandle
end

--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY OR CALL THIS HELPER FUNCTION
**************************************************************
	Function Name : saveTexture()
    Purpose:
	---
	Reads and initializes the applied texture to Base object
    and saves it to a file.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	saveTexture()
**************************************************************	
]]--
function saveTexture()
    baseHandle = sim.getObjectHandle("Base")
    textureID = sim.getShapeTextureId(baseHandle)
    textureData=sim.readTexture(textureID ,0,0,0,0,0)
    sim.saveImage(textureData, {512,512}, 0, "models/other/base_template.png", -1)
end
--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY OR CALL THIS HELPER FUNCTION
**************************************************************
	Function Name : retrieveTexture()
    Purpose:
	---
	Loads texture from file.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	retrieveTexture()
**************************************************************	
]]--
function retrieveTexture()
    textureData, resolution = sim.loadImage(0, "models/other/base_template.png") 
end

--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY OR CALL THIS HELPER FUNCTION
**************************************************************
	Function Name : reapplyTexture()
    Purpose:
	---
	Re-applies texture to Base object

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
    reapplyTexture()
**************************************************************	
]]--
function reapplyTexture()
    plane, textureID = sim.createTexture("", 0, nil, {1.01, 1.01}, nil, 0, {512, 512})
    sim.writeTexture(textureID, 0, textureData, 0, 0, 0, 0, 0)
    sim.setShapeTexture(baseHandle, textureID, sim.texturemap_plane, 0, {1.01, 1.01},nil,nil)
    sim.removeObject(plane)
end

--############################################################

--[[
**************************************************************
	Function Name : receiveData()
    Purpose:
	---
	Receives data via Remote API. This function is called by 
    simx.callScriptFunction() in the python code (task_2b.py)

	Input Arguments:
	---
	inInts : Table of Ints
    inFloats : Table of Floats
    inStrings : Table of Strings
    inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
    inFloats : Table of Floats
    inStrings : Table of Strings
    inBuffer : string
    
    These 4 variables represent the data being passed from remote
    API client(python) to the CoppeliaSim scene
	
	Example call:
	---
	N/A
    
    Hint:
    ---
    You might want to study this link to understand simx.callScriptFunction()
    better 
    https://www.coppeliarobotics.com/helpFiles/en/remoteApiExtension.htm
**************************************************************	
]]--
function receiveData(inInts,inFloats,inStrings,inBuffer)

    --*******************************************************
    --               ADD YOUR CODE HERE
    
    table.insert(maze_array,inInts) -- Inserting data to maze_array received from python remote api
        
    --*******************************************************
    return inInts, inFloats, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : generateHorizontalWalls()
    Purpose:
	---
	Generates all the Horizontal Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	generateHorizontalWalls()
**************************************************************	
]]--
function generateHorizontalWalls()

    --*******************************************************
    --               ADD YOUR CODE HERE
    
    baseHandle=sim.getObjectHandle('Base') --To get base handle
    x=-0.45
    y=0.5
    m=101 
    for i=1,11 do
        for j=1,10 do
            wallHandle=createWall()
            result=sim.setObjectParent(wallHandle,baseHandle,False) --Making 'base' parent of 'wall'
            result=sim.setObjectName(wallHandle,m) --To set name of wall
            result=sim.setObjectPosition(wallHandle,baseHandle,{x,y,0.0650}) --To set the wall's position w.r.t. base
            m=m+1
            x=x+0.1
        end
        y=y-0.1
        x=-0.45
    end


        
    --*******************************************************
end

--[[
**************************************************************
	Function Name : generateVerticalWalls()
    Purpose:
	---
	Generates all the Vertical Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	generateVerticalWalls()
**************************************************************	
]]--
function generateVerticalWalls()

    --*******************************************************
    --               ADD YOUR CODE HERE
    
    baseHandle=sim.getObjectHandle('Base') --To get base handle
    x=-0.5
    y=0.45
    k=301
    for i=1,10 do
        for j=1,11 do
            wallHandle=createWall()
            result=sim.setObjectParent(wallHandle,baseHandle,False) --Making 'base' parent of 'wall'
            result=sim.setObjectName(wallHandle,k) --To set name of wall
            result=sim.setObjectPosition(wallHandle,baseHandle,{x,y,0.0650}) --To set the wall's position w.r.t. base
            result=sim.setObjectOrientation(wallHandle,baseHandle,{0,0,1.57}) --To set orientation of wall
            k=k+1
            x=x+0.1
        end
        y=y-0.1
        x=-0.5
    end
    
    --*******************************************************
end

--[[
**************************************************************
	Function Name : deleteWalls()
    Purpose:
	---
	Deletes all the walls in the given scene

	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	deleteWalls()
**************************************************************	
]]--

function deleteWalls()

    --*******************************************************
    --               ADD YOUR CODE HERE


    --[ This nested function is used to check whether wall is already deleted or not ]--
    local function contains(table,val) 
        for i=1,#table do
            if table[i] == val then 
                return true
            end
        end
        return false
    end


    local table = del_obj
    
    --[ Deleting those horizontal walls which are not already deleted ]--
    a=101
    for i=101,210 do
        if contains(table, a) == false then
            delobj(a)
        end
        a=a+1
    end
    
    --[ Deleting those vertical walls which are not already deleted ]--
    b=301
    for i=301,410 do
        if contains(table, b) == false then
            delobj(b)
        end
        b=b+1
    end
    
    maze_array = {}
    del_obj={}
    table={}
    
    --*******************************************************
end


--[[
**************************************************************
  YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT PARAMETERS FOR THIS
                          FUNCTION
**************************************************************
	Function Name : createMaze()
    Purpose:
	---
	Creates the maze in the given scene by deleting specific 
    horizontal and vertical walls

	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	createMaze()
**************************************************************	
]]--


function createMaze()
    
    --*******************************************************
    --               ADD YOUR CODE HERE
    Hor={}
    Ver={}
    index={}
    
    for u=101,210 do   --To make table of all horizontal walls 
        table.insert(Hor,u)
    end

    for v=301,410 do  --To make table of all vertical walls
        table.insert(Ver,v)
    end

    for i=1,10 do     --This is to get individual element in maze_array later
        table.insert(index,i)
    end
    
    --[ For Creating Maze, deleting unncessary walls ]--
    p={}
    for i=1,10 do
            p=maze_array[i]
            
            --[ Getting individual element from Hor, Ver and index tables simultaneously using zip function in for loop ]-- 
            for a,b,j in zip(Hor,Ver,index) do 
                        if p[j]==0 then
                            --delobj(a)--
                            c=a+10
                            delobj(c)
                            --delobj(b)--
                            d=b+1
                            delobj(d)
                            table.insert(del_obj,c)
                            table.insert(del_obj,d)

                        elseif p[j]==1 then
                            --delobj(a)--
                            c=a+10
                            delobj(c)
                            d=b+1
                            delobj(d)
                            table.insert(del_obj,c)
                            table.insert(del_obj,d)
                    
                        elseif p[j]==2 then
                            c=a+10
                            delobj(c)
                            --delobj(b)--
                            d=b+1
                            delobj(d)
                            table.insert(del_obj,c)
                            table.insert(del_obj,d)
                    
                        elseif p[j]==3 then
                            c=a+10
                            delobj(c)
                            d=b+1
                            delobj(d)
                            table.insert(del_obj,c)
                            table.insert(del_obj,d)
                    
                        elseif p[j]==4 then
                            --delobj(a)--
                            c=a+10
                            delobj(c)
                            ---delobj(b)--
                            table.insert(del_obj,c)
                
                        elseif p[j]==5 then
                            --delobj(a)--
                            c=a+10
                            delobj(c)
                            table.insert(del_obj,c)
                   
                        elseif p[j]==6 then
                            c=a+10
                            delobj(c)
                            --delobj(b)--
                            table.insert(del_obj,c)
                    
                        elseif p[j]==7 then
                            c=a+10
                            delobj(c)
                            table.insert(del_obj,c)

                        elseif p[j]==8 then
                            --delobj(a)--
                            --delobj(b)--
                            d=b+1
                            delobj(d)
                            table.insert(del_obj,d)
                    
                        elseif p[j]==9 then
                            --delobj(a)--
                            d=b+1
                            delobj(d)
                            table.insert(del_obj,d)
                    
                        elseif p[j]==10 then
                            --delobj(b)--
                            d=b+1
                            delobj(d)
                            table.insert(del_obj,d)
                    
                        elseif p[j]==11 then
                            d=b+1
                            delobj(d)
                            table.insert(del_obj,d)
                    
                        elseif p[j]==12 then
                            --delobj(a)--
                            --delobj(b)--
                    
                        elseif p[j]==13 then
                            --delobj(a)--
                    
                        elseif p[j]==14 then
                            --delobj(b)--
                    
                        elseif p[j]==15 then
                        end
            end
            --[ Updating Hor table ]--
            for k=1,10 do
                a=1
                table.remove(Hor,a) 
                a=a+1
            end
            
            --[ Updating Ver table ]--
            for k=1,11 do
                a=1
                table.remove(Ver,a) 
                a=a+1
            end
        
    end
    Hor={}
    Ver={}
end
            
      
    --*******************************************************



--[[
**************************************************************
	Function Name : sysCall_init()
    Purpose:
	---
	Can be used for initialization of parameters
    
	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_init()

    if pcall(saveTexture) then -- Do not delete or modify this section
        print("Successfully saved texture")
    else
        print("Texture does not exist. Importing texture from file..")
        retrieveTexture()
        reapplyTexture()
    end     
end

--[[
**************************************************************
        YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION. 
**************************************************************
	Function Name : sysCall_beforeSimulation()
    Purpose:
	---
	This is executed before simulation starts
    
	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_beforeSimulation()
    
    sim.setShapeTexture(baseHandle, -1, sim.texturemap_plane, 0, {1.01, 1.01},nil,nil) -- Do not delete or modify this line
    
    generateHorizontalWalls()
    generateVerticalWalls()
    createMaze()
end

--[[
**************************************************************
        YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION. 
**************************************************************
	Function Name : sysCall_afterSimulation()
    Purpose:
	---
	This is executed after simulation ends
    
	Input Arguments:
	---
	None
	
	Returns:
	---
    None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_afterSimulation()
    -- is executed after a simulation ends
    deleteWalls()
    reapplyTexture() -- Do not delete or modify this line
end

function sysCall_cleanup()
    -- do some clean-up here
end

-- See the user manual or the available code snippets for additional callback functions and details




