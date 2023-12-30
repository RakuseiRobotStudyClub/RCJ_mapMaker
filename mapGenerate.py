VERSION=0.8
#import
import os
import sys
import pygame
from pygame.locals import *
import json
import tkinter as tk
from tkinter import filedialog
import openpyxl
import shutil
#keys
keyDown=0
keyDownM=0
keyLeftP=0
keyRightP=0
keyRight=0
keyLeft=0
keyUp=0
keyC=0
keyZ=0
keyX=0
keyL=0
keyO=0
keyR=0
keyP=0
keyQ=0
keyA=0
keyW=0
keyS=0
keyT=0
keyE=0
keyM=0
keyN=0
key0=0
key1=0
key2=0
key3=0
key4=0
key5=0
key6=0
key7=0
key8=0
key9=0
keyShift=0
keyEsc=0
keyCtrl=0
mouseButtonDown=0
mouseButtonUp=0
mouseButtonLeft=0
mouseButtonRight=0
def getkeys():
    global key0,key1,key2,key3,key4,key5,key6,key7,key8,key9,keyDown,keyLeftP,keyRightP,keyRight,keyLeft,keyZ,keyUp,keyX,keyC,keyR,keyQ,keyE,keyW,keyT,keyShift,keyEsc,mouseButtonDown,mouseButtonUp,keyCtrl,keyS,keyL,keyP,keyA,mouseButtonRight,mouseButtonLeft,keyM,keyO,keyN
    #key1=0
    key0=0
    key1=0
    key2=0
    key3=0
    key4=0
    key5=0
    key6=0
    key7=0
    key8=0
    key9=0
    keyDown=0
    keyRight=0
    keyLeft=0
    keyUp=0
    keyC=0
    keyR=0
    keyS=0
    keyA=0
    keyL=0
    keyT=0
    keyP=0
    keyZ=0
    keyX=0
    keyQ=0
    keyW=0
    keyE=0
    keyM=0
    keyO=0
    keyN=0
    keyEsc=0
    mouseButtonDown=0
    mouseButtonUp=0
    mouseButtonRight=0
    mouseButtonLeft=0
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_0:key0=1
            if event.key == K_1:key1=1
            if event.key == K_2:key2=1
            if event.key == K_3:key3=1
            if event.key == K_4:key4=1
            if event.key == K_5:key5=1
            if event.key == K_6:key6=1
            if event.key == K_7:key7=1
            if event.key == K_8:key8=1
            if event.key == K_9:key9=1
            if event.key == K_DOWN:keyDown=1
            if event.key == K_UP: keyUp=1
            if event.key == K_RIGHT: 
                keyRight=1
                keyRightP=1
            if event.key == K_LEFT:
                keyLeft=1
                keyLeftP=1
            if event.key == K_z: keyZ=1
            if event.key == K_x: keyX=1
            if event.key == K_c: keyC=1
            if event.key == K_r: keyR=1
            if event.key == K_q: keyQ=1
            if event.key == K_a: keyA=1
            if event.key == K_m: keyM=1
            if event.key == K_p: keyP=1
            if event.key == K_w: keyW=1
            if event.key == K_s: keyS=1
            if event.key == K_l: keyL=1
            if event.key == K_t: keyT=1
            if event.key == K_e: keyE=1
            if event.key == K_o: keyO=1
            if event.key == K_n: keyN=1
            if event.key == K_LSHIFT:keyShift=1
            if event.key == K_ESCAPE:keyEsc=1
            if event.key == K_LCTRL:keyCtrl=1
        if event.type == KEYUP:
            if event.key == K_RIGHT: keyRightP=0
            if event.key == K_LEFT: keyLeftP=0
            if event.key == K_LSHIFT:keyShift=0
            if event.key == K_LCTRL:keyCtrl=0
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:mouseButtonLeft=1
            if event.button == 3:mouseButtonRight=1
            if event.button == 4:mouseButtonDown=1
            if event.button == 5:mouseButtonUp=1
        #if event.type == MOUSEBUTTONUP:
            #mouseButtonUp=1
color_white=(255,255,255)
color_gray=(100,100,100)
color_red=(255,0,0)
color_orange=(255,100,0)
color_yellow=(255,255,0)
color_palegolden=(128,124,91)
color_palegoldenblack=(78,74,41)
color_black=(0,0,0)
#load config
with open("config.json") as f:
    _b=f.read()
    _b = json.loads(_b)
    MAPX=_b['mapx']
    MAPY=_b['mapy']
    BLOCKSIZE=_b['blocksizeView']
    BLOCKSIZE2=_b['blocksizePrint']
pygame.init()
screen = pygame.display.set_mode((BLOCKSIZE*(MAPX),BLOCKSIZE*(MAPY+6)))
pygame.display.set_caption("LineMapMaker")
pygame.display.set_icon(pygame.image.load("icon.png"))
#menu init
selectTileX,selectTileY=0,0
selectTileId=1
selectTileIdMenu=1
selectTileIdMenuAd=1
selectTileDir=0
selectTileType=0 #0:nomal 1:ad 2:rescueArea
selectTileMenuTable=0
selectTileMenuTableAd=0
outCursor=False
TABLEMAX=4
TABLEMAXAD=4
input_active = False
menuFont = pygame.font.SysFont("Arial", BLOCKSIZE)
menuMiniFont = pygame.font.SysFont("Arial", int(BLOCKSIZE/2))
debugFont = pygame.font.SysFont("Arial", int(BLOCKSIZE/4))
debugText=""
TILETYPENONE=0
TILETYPENOMAL=1
TILETYPEAD=2
TILETYPEAREA=3
#load img
tileImages=[]
adtileImages=[]
rescueAreaImages=[]
imgErase=pygame.transform.scale(pygame.image.load("erase.png"), (BLOCKSIZE,BLOCKSIZE))
#file init
fieldMap=[[[[0,0,0]] for j in range(MAPY)] for k in range(MAPX)]
'''
fieldmap[x][y]=[[maintile],[adtile1],[adtile2]...]
[tile]=[type,id,dir]
'''
fileName="undefined00"
FIELDTYPES=["WRL","NERL","WRM","NERM"]
fieldType=0 # WRL,NERL,WRM,NERM
def loadTileimg():
    global tileImages,adtileImages,rescueAreaImages
    tileImages=[]
    _fileList=[]
    for file in os.listdir("./tile"):
        base, ext = os.path.splitext(file)
        if ext == '.png':
            #print('file:{},ext:{}'.format(file,ext))
            _fileList.append('./tile/{}'.format(file))
    for i in _fileList:
        tileImages.append(pygame.transform.scale(pygame.image.load(i), (BLOCKSIZE,BLOCKSIZE)))
    adtileImages=[]
    _fileList=[]
    for file in os.listdir("./additionTile"):
        base, ext = os.path.splitext(file)
        if ext == '.png':
            #print('file:{},ext:{}'.format(file,ext))
            _fileList.append('./additionTile/{}'.format(file))
    for i in _fileList:
        adtileImages.append(pygame.transform.scale(pygame.image.load(i), (BLOCKSIZE,BLOCKSIZE)))
    rescueAreaImages=[]
    _fileList=[]
    for file in os.listdir("./rescueArea"):
        base, ext = os.path.splitext(file)
        if ext == '.png':
            #print('file:{},ext:{}'.format(file,ext))
            _fileList.append('./rescueArea/{}'.format(file))
    for i in _fileList:
        rescueAreaImages.append(pygame.transform.scale(pygame.image.load(i), (BLOCKSIZE*4,BLOCKSIZE*3)))
loadTileimg()
TABLEMAX=int(len(tileImages)/10)+1
TABLEMAXAD=int(len(adtileImages)/10)+1
#main
while True:
    ###inputs
    if not input_active:getkeys()
    mouseX,mouseY=pygame.mouse.get_pos()    
    mouseLeft,mouseMIddle,mouseRight=pygame.mouse.get_pressed()
    #cursor
    outCursor=False
    selectTileY=int((mouseY-BLOCKSIZE)/BLOCKSIZE)
    if selectTileY<0 or mouseY<BLOCKSIZE:
        selectTileY=0
        outCursor=True
    if selectTileY>MAPY-1:
        selectTileY=MAPY-1
        outCursor=True
    selectTileX=int(mouseX/BLOCKSIZE)
    if selectTileX<0:
        selectTileX=0
        outCursor=True
    if selectTileX>MAPX-1:
        selectTileX=MAPX-1
        outCursor=True
    #drawtile
    if mouseLeft and not outCursor:
        if selectTileType==0:#nomal
            fieldMap[selectTileX][selectTileY][0]=[TILETYPENOMAL,selectTileId,selectTileDir]
        if selectTileType==1 and mouseButtonLeft:#ad
            fieldMap[selectTileX][selectTileY].append([TILETYPEAD,selectTileId,selectTileDir])
        if selectTileType==2 and mouseButtonLeft:#rescueArea
            fieldMap[selectTileX][selectTileY].append([TILETYPEAREA,selectTileId,selectTileDir])
    #del tile
    if mouseRight:
        fieldMap[selectTileX][selectTileY]=[[TILETYPENONE,0,0]]
    #rotate
    if keyR:
        selectTileDir+=1
        if selectTileDir==4:
            selectTileDir=0
    #input name
    if mouseLeft and mouseY<BLOCKSIZE:
        input_active = True
    if input_active:
        outCursor=True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    fileName =  fileName[:-1]
                else:
                    fileName += event.unicode
    if mouseLeft and mouseY>BLOCKSIZE:
        input_active=False
    #selectTile
    if keyShift:#adtile
        if key1:
            _n=1+selectTileMenuTableAd*10
        if key2:
            _n=2+selectTileMenuTableAd*10
        if key3:
            _n=3+selectTileMenuTableAd*10
        if key4:
            _n=4+selectTileMenuTableAd*10
        if key5:
            _n=5+selectTileMenuTableAd*10
        if key6:
            _n=6+selectTileMenuTableAd*10
        if key7:
            _n=7+selectTileMenuTableAd*10
        if key8:
            _n=8+selectTileMenuTableAd*10
        if key9:
            _n=9+selectTileMenuTableAd*10
        if key0:
            _n=10+selectTileMenuTableAd*10
        #1-0key
        if(key0 or key1 or key2 or key3 or key4 or key5 or key6 or key7 or key8 or key9) and len(adtileImages)>=_n:
            #selectTileId=_n
            selectTileIdMenuAd=_n
            selectTileType=1
        #mouse ud
        if (mouseButtonUp or mouseButtonDown) and selectTileType!=1:
            #selectTileId=1
            selectTileType=1
        if mouseButtonDown and len(adtileImages)>=selectTileIdMenuAd+1:
            #selectTileId+=1
            selectTileIdMenuAd+=1
            if (selectTileMenuTableAd+1)*10<selectTileIdMenuAd:selectTileMenuTableAd+=1
        if mouseButtonUp and 0<selectTileIdMenuAd-1:
            #selectTileId-=1
            selectTileIdMenuAd-=1
            if selectTileMenuTableAd*10>=selectTileIdMenuAd:selectTileMenuTableAd-=1
        if selectTileType==1:selectTileId=selectTileIdMenuAd
    elif keyCtrl: #rescueArea
        if key1:
            _n=1
        if key2:
            _n=2
        if key3:
            _n=3
        if key4:
            _n=4
        if key5:
            _n=5
        if key6:
            _n=6
        if key7:
            _n=7
        if key8:
            _n=8
        if key9:
            _n=9
        if key0:
            _n=10
        if(key0 or key1 or key2 or key3 or key4 or key5 or key6 or key7 or key8 or key9) and len(rescueAreaImages)>=_n:
            selectTileId=_n
            selectTileType=2
        if (mouseButtonUp or mouseButtonDown) and selectTileType!=2:
            selectTileId=1
            selectTileType=2
        if mouseButtonDown and len(rescueAreaImages)>=selectTileId+1:
            selectTileId+=1
        if mouseButtonUp and 0<selectTileId-1:
            selectTileId-=1
    else:#nomaltile
        if key1:
            _n=1+selectTileMenuTable*10
        if key2:
            _n=2+selectTileMenuTable*10
        if key3:
            _n=3+selectTileMenuTable*10
        if key4:
            _n=4+selectTileMenuTable*10
        if key5:
            _n=5+selectTileMenuTable*10
        if key6:
            _n=6+selectTileMenuTable*10
        if key7:
            _n=7+selectTileMenuTable*10
        if key8:
            _n=8+selectTileMenuTable*10
        if key9:
            _n=9+selectTileMenuTable*10
        if key0:
            _n=10+selectTileMenuTable*10
        if  (key0 or key1 or key2 or key3 or key4 or key5 or key6 or key7 or key8 or key9) and len(tileImages)>=_n:
            selectTileIdMenu=_n
            selectTileType=0
        if (mouseButtonUp or mouseButtonDown) and selectTileType!=0:
            #selectTileId=1
            #selectTileMenuTable=0
            selectTileType=0
        if mouseButtonDown and len(tileImages)>=selectTileIdMenu+1:
            selectTileIdMenu+=1
            if (selectTileMenuTable+1)*10<selectTileIdMenu:selectTileMenuTable+=1
        if mouseButtonUp and 0<selectTileIdMenu-1:
            selectTileIdMenu-=1
            if selectTileMenuTable*10>=selectTileIdMenu:selectTileMenuTable-=1
        if selectTileType==0: selectTileId=selectTileIdMenu
    #selectMenuTable
    if keyE or keyQ:
        if keyShift:
            selectTileType=1
            if keyE:
                selectTileMenuTableAd+=1
                if selectTileMenuTableAd>=TABLEMAXAD-1:selectTileMenuTableAd=TABLEMAXAD-2
                selectTileIdMenuAd=selectTileMenuTableAd*10+1
                selectTileId=selectTileIdMenuAd
            if keyQ:
                selectTileMenuTableAd-=1
                if selectTileMenuTableAd<0:selectTileMenuTableAd=0
                selectTileIdMenuAd=selectTileMenuTableAd*10+1
                selectTileId=selectTileIdMenuAd
        else:
            selectTileType=0
            if keyE:
                selectTileMenuTable+=1
                if selectTileMenuTable>=TABLEMAX-1:selectTileMenuTable=TABLEMAX-2
                selectTileIdMenu=selectTileMenuTable*10+1
                selectTileId=selectTileIdMenu
            if keyQ:
                selectTileMenuTable-=1
                if selectTileMenuTable<0:selectTileMenuTable=0
                selectTileIdMenu=selectTileMenuTable*10+1
                selectTileId=selectTileIdMenuAd
    #copy
    if keyT:
        _n=fieldMap[selectTileX][selectTileY][0]
        if _n[0]!=0:
            selectTileId=int(_n[1])
            selectTileDir=int(_n[2])
    #change type
    if keyA:
        fieldType+=1
        if fieldType>=len(FIELDTYPES):
            fieldType=0
    #reload textures
    if keyZ:
        loadTileimg()
        TABLEMAX=int(len(tileImages)/10)+1
    #savefile
    if keyCtrl and keyS:
        _di={
            "name":fileName,
            "type":fieldType,
            "map":fieldMap,
            "mapx":MAPX,
            "mapy":MAPY,
            "ver":VERSION,
        }
        if not os.path.isdir("./userfile/"+fileName):os.mkdir("./userfile/"+fileName)
        with open("./userfile/"+fileName+"/"+fileName+".json", 'wt') as f:
            json.dump(_di, f)
        debugText="saved file ["+fileName+"]"
    #loadfile
    if keyCtrl and keyO:
        root=tk.Tk()
        root.withdraw()
        _typ = [('jsonファイル','*.json')] 
        _dir = './userfile'
        fle = filedialog.askopenfilename(filetypes = _typ, initialdir = _dir)
        if fle=="":
            debugText="load file was canceled"
        else:
            with open(fle) as f:
                _b=f.read()
                _b = json.loads(_b)
                _mapx=_b['mapx']
                _mapy=_b['mapy']
                if (_mapx==MAPX and _mapy==MAPY):
                    fileName=_b['name']
                    fieldType=_b['type']
                    fieldMap=_b['map']
                    _fileVer=_b['ver']    
                    debugText="loaded file ["+fileName+"]"
                    if _fileVer > VERSION:
                        debugText="warn: this file was made on newer version."
                    if _fileVer != VERSION:
                        debugText="warn: this file was made on lower version."
                else:
                    debugText="error: this map's size is not match."
    #print file
    if keyCtrl and keyP:
        #create img
        screen2 = pygame.display.set_mode((BLOCKSIZE2*(MAPX),BLOCKSIZE2*(MAPY)))
        pygame.draw.rect(screen2,color_palegolden,(0,0,BLOCKSIZE2*(MAPX),BLOCKSIZE2*(MAPY)))
        for y in range(int(MAPY)):
            for x in range(int(MAPX)):
                pygame.draw.rect(screen2,color_gray,(x*BLOCKSIZE2+2,(y)*BLOCKSIZE2+2,BLOCKSIZE2-4,BLOCKSIZE2-4))
        for y in range(int(MAPY)):
            for x in range(int(MAPX)):
                for i in range(len(fieldMap[x][y])):
                    if fieldMap[x][y][i][0]==TILETYPENONE:
                        pass
                    elif fieldMap[x][y][i][0]==TILETYPENOMAL:
                        screen2.blit(pygame.transform.rotate(tileImages[int(fieldMap[x][y][i][1]-1)],int(90*fieldMap[x][y][i][2])),(x*BLOCKSIZE,(y+1)*BLOCKSIZE))
                    elif fieldMap[x][y][i][0]==TILETYPEAD:
                        screen2.blit(pygame.transform.rotate(adtileImages[int(fieldMap[x][y][i][1]-1)],int(90*fieldMap[x][y][i][2])),(x*BLOCKSIZE,(y+1)*BLOCKSIZE))
                    elif fieldMap[x][y][i][0]==TILETYPEAREA:
                        screen2.blit(pygame.transform.rotate(rescueAreaImages[int(fieldMap[x][y][i][1]-1)],int(90*fieldMap[x][y][i][2])),(x*BLOCKSIZE,(y+1)*BLOCKSIZE))
        #create dir if there isn't
        _filedir="./userfile/"+fileName
        _pngpass=_filedir+"/"+fileName+".png"
        _xlsxpass=_filedir+"/"+fileName+".xlsx"
        if not os.path.isdir(_filedir):os.mkdir(_filedir)
        pygame.image.save(screen2,_pngpass)
        del(screen2)
        screen = pygame.display.set_mode((BLOCKSIZE*(MAPX),BLOCKSIZE*(MAPY+6)))
        #create xlsx if there isn't
        if not os.path.isfile(_xlsxpass):
            shutil.copyfile("plain-"+FIELDTYPES[fieldType]+".xlsx",_xlsxpass)
        #print img to xlsx
        workbook = openpyxl.load_workbook(_xlsxpass)
        sheet    = workbook.active
        img_to_excel = openpyxl.drawing.image.Image(_pngpass)
        sheet.add_image(img_to_excel, 'A1')
        workbook.save(_xlsxpass)
        debugText="printed file ["+fileName+"]"
    #new file
    if keyCtrl and keyN:
        fileName="undefined00"
        fieldType=0
        fieldMap=[[[[0,0,0]] for j in range(MAPY)] for k in range(MAPX)]
    #exit
    '''if keyEsc:
        break'''
    ###draw
    #fill
    pygame.draw.rect(screen,color_palegolden,(0,0,BLOCKSIZE*(MAPX),BLOCKSIZE*(MAPY+7)))
    pygame.draw.rect(screen,color_palegoldenblack,(0,BLOCKSIZE*(MAPY+1),BLOCKSIZE*(MAPX),BLOCKSIZE*(MAPY+7)))
    #draw title
    if input_active:pygame.draw.rect(screen,color_orange,(0,BLOCKSIZE*(0),BLOCKSIZE*(MAPX),BLOCKSIZE*(1)))
    screen.blit(menuFont.render(fileName, True, color_white), (0,0))
    screen.blit(menuFont.render(FIELDTYPES[fieldType], True, color_white), (BLOCKSIZE*(MAPX-3),0))
    #draw main
    for y in range(int(MAPY)):
        for x in range(int(MAPX)):
            pygame.draw.rect(screen,color_gray,(x*BLOCKSIZE+2,(y+1)*BLOCKSIZE+2,BLOCKSIZE-4,BLOCKSIZE-4))
    for y in range(int(MAPY)):
        for x in range(int(MAPX)):
            for i in range(len(fieldMap[x][y])):
                if fieldMap[x][y][i][0]==TILETYPENONE:
                    pass
                elif fieldMap[x][y][i][0]==TILETYPENOMAL:
                    screen.blit(pygame.transform.rotate(tileImages[int(fieldMap[x][y][i][1]-1)],int(90*fieldMap[x][y][i][2])),(x*BLOCKSIZE,(y+1)*BLOCKSIZE))
                elif fieldMap[x][y][i][0]==TILETYPEAD:
                    screen.blit(pygame.transform.rotate(adtileImages[int(fieldMap[x][y][i][1]-1)],int(90*fieldMap[x][y][i][2])),(x*BLOCKSIZE,(y+1)*BLOCKSIZE))
                elif fieldMap[x][y][i][0]==TILETYPEAREA:
                    screen.blit(pygame.transform.rotate(rescueAreaImages[int(fieldMap[x][y][i][1]-1)],int(90*fieldMap[x][y][i][2])),(x*BLOCKSIZE,(y+1)*BLOCKSIZE))
    #drawselecting
    if not outCursor:
        if mouseRight:_im=imgErase
        elif selectTileType==0:_im=pygame.transform.rotate(tileImages[selectTileId-1], 90*selectTileDir)
        elif selectTileType==1:_im=pygame.transform.rotate(adtileImages[selectTileId-1], 90*selectTileDir)
        elif selectTileType==2:_im=pygame.transform.rotate(rescueAreaImages[selectTileId-1], 90*selectTileDir)
        screen.blit(_im,(selectTileX*BLOCKSIZE,(selectTileY+1)*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE))
    #draw fotter
    for i in range(10):#maintile
        _n=i+selectTileMenuTable*10
        if len(tileImages)>_n:
            _c=color_yellow
            if selectTileType==0:_c=color_orange
            if(selectTileMenuTable*10<=selectTileIdMenu and selectTileIdMenu<=(selectTileMenuTable+1)*10)and(selectTileIdMenu%10-1==i or (selectTileIdMenu%10==0 and i==9)):pygame.draw.rect(screen,_c,(BLOCKSIZE*i*1.1,BLOCKSIZE*(MAPY+2),BLOCKSIZE,BLOCKSIZE))
            screen.blit(tileImages[_n],(BLOCKSIZE*i*1.1,BLOCKSIZE*(MAPY+1)))     
    screen.blit(menuMiniFont.render(""+str(selectTileType), True, color_white), (BLOCKSIZE*(10)*1.1,BLOCKSIZE*(MAPY+1)))
    screen.blit(menuMiniFont.render(""+str(selectTileId), True, color_white), (BLOCKSIZE*(10)*1.1,BLOCKSIZE*(MAPY+1.5)))
    for i in range(10):#adtile
        _n=i+selectTileMenuTableAd*10
        if len(adtileImages)>_n:
            _c=color_yellow
            if selectTileType==1:_c=color_orange
            if(selectTileMenuTableAd*10<=selectTileIdMenuAd and selectTileIdMenuAd<=(selectTileMenuTableAd+1)*10)and(selectTileIdMenuAd%10-1==i or (selectTileIdMenuAd%10==0 and i==9)):pygame.draw.rect(screen,_c,(BLOCKSIZE*i*1.1,BLOCKSIZE*(MAPY+3),BLOCKSIZE,BLOCKSIZE))
            screen.blit(adtileImages[_n],(BLOCKSIZE*i*1.1,BLOCKSIZE*(MAPY+3)))
    for i in range(10):#rescueArea
        if len(rescueAreaImages)>i:
            if selectTileType==2:
                if selectTileId-1==i:pygame.draw.rect(screen,color_orange,(BLOCKSIZE*i*1.6,BLOCKSIZE*(MAPY+4),BLOCKSIZE*1.6,BLOCKSIZE*2))
            screen.blit(pygame.transform.scale(rescueAreaImages[i],(BLOCKSIZE*1.6,BLOCKSIZE*1.2)),(BLOCKSIZE*i*1.6,BLOCKSIZE*(MAPY+4)))
    for i in range(10):
        _t=i+1
        if i==9:_t=0
        screen.blit(menuFont.render(str(_t), True, color_white), (BLOCKSIZE*i*1.1,BLOCKSIZE*(MAPY+2)))    
    screen.blit(debugFont.render("Id"+str(selectTileId)+",Dir:"+str(selectTileDir)+",Type:"+str(selectTileType)+",Table:"+str(selectTileMenuTable), True, color_white), (BLOCKSIZE*(8),BLOCKSIZE*(MAPY+4)))
    screen.blit(debugFont.render(str((selectTileX,selectTileY))+":"+str(fieldMap[selectTileX][selectTileY]), True, color_white), (BLOCKSIZE*(8),BLOCKSIZE*(MAPY+4.25)))
    screen.blit(debugFont.render(debugText, True, color_white), (BLOCKSIZE*(8),BLOCKSIZE*(MAPY+4.5)))
    screen.blit(menuMiniFont.render("ver:"+str(VERSION), True, color_white), (BLOCKSIZE*(MAPX-2),BLOCKSIZE*(MAPY+5)))
    pygame.display.update()