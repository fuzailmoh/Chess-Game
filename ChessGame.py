from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from enum import Enum

#import all neccessary Packages from Python

#WHAT TO DO WHEN YOU GET BACK
#1. Fix the button disabled and !disabled once button is clicked (work out the logic) - SOLVED use individual functions, Check One note for lofic
#2. Figure out the ReRouting of the page to the ChessPage - Use PannedWindow implementation
class GameState(Enum):
    WELCOMEPAGE = 0
    WAIT1 = 1
    PLANMOVE1 = 2
    WAIT2 = 3
    PLANMOVE2 = 4
    INCHECKWAIT1 = 5
    INCHECKWAIT2 = 6
    INCHECKPLAN1 = 7
    INCHECKPLAN2 = 8

class ChessGame():

    P1Color = ""
    P2Color = ""
    P1Pass = ""
    P2Pass = ""
    P1UserName = ""
    P2UserName = ""
    state = GameState.WELCOMEPAGE
    pieceToMove = None
    P1KING = None
    P2KING = None
    topLevelFrame = None
    
    

    def __init__(self, master):
        #Intialize Welcome Page with Frames and pack them to root page
        ChessGame.topLevelFrame = master
        master.title('NoviceKnight Chess')
        
        master.minsize(1040,380)

        #Intializing Style Object
        self.style = ttk.Style()
        self.style.theme_use('classic')

        #Creating a notebook
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill = BOTH, expand = TRUE)

        #Creating Frames two pages
        self.welcomePage = ttk.Frame(self.notebook)
        self.gamePage = ttk.Frame(self.notebook)

        #adding the welcome page
        self.notebook.add(self.welcomePage, text = 'Welcome Page')

        #Frames for Welcome Page
        self.headerFrame = ttk.Frame(self.welcomePage)
        self.userChoiceFrame = ttk.Frame(self.welcomePage)
        
        #pack the frames
        self.headerFrame.pack(fill = BOTH, expand = True)
        self.userChoiceFrame.pack(fill = BOTH, expand = True)

        #add the three labels in the header frame
        #have to do some manuvering to solve subsample issue with PIL (PIL does not allow subsampling to make image smaller)
        self.whitePiece = Image.open('ChessGame/WhiteChessPiece.png')
        (self.x0w,self.y0w,self.x1w,self.y1w) = self.whitePiece.getbbox() # returns (0,0,w,h)
        self.whitePiece.thumbnail((1+self.x1w/5,1+self.y1w/5)) # changes image in place!
        self.imgWP=ImageTk.PhotoImage(self.whitePiece)


        self.blackPiece = Image.open('ChessGame/BlackChessPiece.png')
        (self.x0b, self.y0b, self.x1b, self.y1b) = self.blackPiece.getbbox()
        self.blackPiece.thumbnail((1+self.x1b/5,1+self.y1b/5))
        self.imgBP = ImageTk.PhotoImage(self.blackPiece)
        
        
        ttk.Label(self.headerFrame, image = self.imgWP).pack(side = LEFT, expand = TRUE)
        ttk.Label(self.headerFrame, text = "Welcome to NoviceKnight Chess, Chess for beginners", font= ('Courier', 22), background = 'light blue').pack(side=LEFT)
        ttk.Label(self.headerFrame, image = self.imgBP).pack(side = LEFT, expand = TRUE)

        #Widgets for the userChoice Frame. Add the two Labels, 7 buttons and 2 entry boxes
        ttk.Label(self.userChoiceFrame, text = 'Player 1 Choose Color').grid(row = 0, column = 0, columnspan = 5)
        ttk.Label(self.userChoiceFrame, text = 'Player 2 Choose Color').grid(row = 0, column = 6, columnspan = 5)


        self.userChoiceFrame.rowconfigure(0, weight = 1)
        self.userChoiceFrame.columnconfigure(0, weight = 1)
        self.userChoiceFrame.columnconfigure(1, weight = 1)
        self.userChoiceFrame.columnconfigure(2, weight = 1)
        self.userChoiceFrame.columnconfigure(3, weight = 1)
        self.userChoiceFrame.columnconfigure(4, weight = 1)
        self.userChoiceFrame.columnconfigure(5, weight = 1)
        self.userChoiceFrame.columnconfigure(6, weight = 1)
        self.userChoiceFrame.columnconfigure(7, weight = 1)
        self.userChoiceFrame.columnconfigure(8, weight = 1)
        self.userChoiceFrame.columnconfigure(9, weight = 1)
        self.userChoiceFrame.columnconfigure(10, weight = 1)

        #Adding White, Black, green styles
        self.style.configure('WC.TButton', background = 'white', foreground = 'black')
        self.style.configure('BC.TButton', background = 'black', foreground = 'white')
        self.style.configure('GC.TButton', background = 'green', foreground = 'white')
        self.style.configure('RC.TButton', background = 'Red', foreground = 'white')
        self.style.configure('GoC.TButton', background = 'gold', foreground = 'white')

        self.style.map('WC.TButton', background = [('active', 'bisque4'), ('disabled','azure3')], foreground = [('active', 'black'), ('disabled','azure2')])
        self.style.map('BC.TButton', background = [('active', 'bisque4'), ('disabled','azure3')], foreground = [('active', 'black'), ('disabled','azure2')])
        self.style.map('GC.TButton', background = [('active', 'bisque4'), ('disabled','azure3')], foreground = [('active', 'black'), ('disabled','azure2')])
        self.style.map('RC.TButton', background = [('active', 'bisque4'), ('disabled','azure3')], foreground = [('active', 'black'), ('disabled','azure2')])
        self.style.map('GoC.TButton', background = [('active', 'bisque4'), ('disabled','azure3')], foreground = [('active', 'black'), ('disabled','azure2')])

        self.P1WhiteB = ttk.Button(self.userChoiceFrame, text = 'White', command = lambda: self.centralButtonCommand(self.P1WhiteB), style = 'WC.TButton')
        self.P1WhiteB.grid(row = 1, column = 0)
        self.P2WhiteB = ttk.Button(self.userChoiceFrame, text = 'White', command = lambda: self.centralButtonCommand(self.P2WhiteB), style = 'WC.TButton')
        self.P2WhiteB.grid(row = 1, column = 6)

        self.P1BlackB = ttk.Button(self.userChoiceFrame, text = 'Black', command = lambda: self.centralButtonCommand(self.P1BlackB), style = 'BC.TButton')
        self.P1BlackB.grid(row = 1, column = 1)
        self.P2BlackB = ttk.Button(self.userChoiceFrame, text = 'Black', command = lambda: self.centralButtonCommand(self.P2BlackB), style = 'BC.TButton')
        self.P2BlackB.grid(row = 1, column = 7)

        self.P1GreenB = ttk.Button(self.userChoiceFrame, text = 'Green', command = lambda: self.centralButtonCommand(self.P1GreenB), style = 'GC.TButton')
        self.P1GreenB.grid(row = 1, column = 2)
        self.P2GreenB = ttk.Button(self.userChoiceFrame, text = 'Green', command = lambda: self.centralButtonCommand(self.P2GreenB), style = 'GC.TButton')
        self.P2GreenB.grid(row = 1, column = 8)

        self.P1RedB = ttk.Button(self.userChoiceFrame, text = 'Red', command = lambda: self.centralButtonCommand(self.P1RedB), style = 'RC.TButton')
        self.P1RedB.grid(row = 1, column = 3)
        self.P2RedB = ttk.Button(self.userChoiceFrame, text = 'Red', command = lambda: self.centralButtonCommand(self.P2RedB), style = 'RC.TButton')
        self.P2RedB.grid(row = 1, column = 9)

        self.P1GoldB = ttk.Button(self.userChoiceFrame, text = 'Gold', command = lambda: self.centralButtonCommand(self.P1GoldB), style = 'GoC.TButton')
        self.P1GoldB.grid(row = 1, column = 4)
        self.P2GoldB = ttk.Button(self.userChoiceFrame, text = 'Gold', command = lambda: self.centralButtonCommand(self.P2GoldB), style = 'GoC.TButton')
        self.P2GoldB.grid(row = 1, column = 10)

        self.submit = ttk.Button(self.userChoiceFrame, text = "Let's Chess!!!", command = self.submit)
        self.submit.grid(row = 3, column = 5, pady = 10, rowspan = 4)
        
        ttk.Label(self.userChoiceFrame, text = 'Pick Name').grid(row = 3, column = 0, columnspan = 5)
        self.P1UserName = ttk.Entry(self.userChoiceFrame)
        self.P1UserName.grid(row = 4, column = 0, columnspan = 5)
        ttk.Label(self.userChoiceFrame, text = 'Pick Name').grid(row = 3, column = 6, columnspan = 5)
        self.P2UserName = ttk.Entry(self.userChoiceFrame)
        self.P2UserName.grid(row = 4, column = 6, columnspan = 5)

        ttk.Label(self.userChoiceFrame, text = 'Surrender Password').grid(row = 5, column = 0, columnspan = 5)
        self.P1PasswordValue = ttk.Entry(self.userChoiceFrame, show = '*')
        self.P1PasswordValue.grid(row = 6, column = 0, columnspan = 5)
        ttk.Label(self.userChoiceFrame, text = 'Surrender Password').grid(row = 5, column = 6, columnspan = 5)
        self.P2PasswordValue = ttk.Entry(self.userChoiceFrame, show = '*')
        self.P2PasswordValue.grid(row = 6, column = 6, columnspan = 5)

        #NOTEE: REMOVE THE CODE BELOW, ONLY HERE FOR TESTING
        #self.notebook.tab(0, state = 'hidden')
        #self.notebook.insert(END, self.gamePage, text = 'Game Page')
        #Code ends here

        #start adding All the Frames, need 7 Frames
        self.headerGPFrame = ttk.Frame(self.gamePage)
        self.P1Frame = ttk.Frame(self.gamePage)
        self.P2Frame = ttk.Frame(self.gamePage)
        self.CBFrame = ttk.Frame(self.gamePage)
        self.LogFrame = ttk.Frame(self.gamePage)
        self.buttonsFrame = ttk.Frame(self.gamePage)

        #dispaly the frames on the game page
        self.headerGPFrame.grid(row = 0, column = 0, columnspan = 3)
        self.P1Frame.grid(row = 1, column = 0)
        self.P2Frame.grid(row = 1, column = 2)
        self.CBFrame.grid(row = 1, column = 1, rowspan = 2)
        self.LogFrame.grid(row = 2, column = 0)
        self.buttonsFrame.grid(row = 2, column = 2)

        self.gamePage.rowconfigure(0, weight = 1)
        self.gamePage.rowconfigure(1, weight= 1)
        self.gamePage.rowconfigure(2, weight = 1)
        self.gamePage.columnconfigure(0, weight= 1)
        self.gamePage.columnconfigure(1, weight= 1)
        self.gamePage.columnconfigure(2, weight= 1)

        #add three label widgets to the header 
        ttk.Label(self.headerGPFrame, image = self.imgWP).pack(side = LEFT)
        self.GPHeaderTitle = ttk.Label(self.headerGPFrame, font = ('Courier', 22), background = 'light blue')
        self.GPHeaderTitle.pack(side = LEFT)
        ttk.Label(self.headerGPFrame, image = self.imgBP).pack(side = LEFT)

        #add the widgets for the P1GFrame 
        self.P1Hist = Text(self.P1Frame, width = 30, height = 7, wrap = 'word')
        self.P1Hist.grid(row = 1, column = 0, columnspan = 2)
        self.Glight = PhotoImage(file = 'ChessGame/GreenLight.gif').subsample(40, 40)
        self.P1Turn = ttk.Label(self.P1Frame, image = self.Glight)
        self.P1Turn.grid(row = 0, column = 1)

        self.P1Frame.rowconfigure(0, weight=1)
        self.P1Frame.rowconfigure(1, weight=1)
        self.P1Frame.columnconfigure(0, weight=1)
        self.P1Frame.columnconfigure(1, weight=1)


        #add the widgets for the P2GFrame
        self.P2Hist = Text(self.P2Frame, width = 30, height = 7, wrap = 'word')
        self.P2Hist.grid(row = 1, column = 0, columnspan = 2)
        self.Rlight = PhotoImage(file = 'ChessGame/RedLight.gif').subsample(27, 27)
        self.P2Turn = ttk.Label(self.P2Frame, image = self.Rlight)
        self.P2Turn.grid(row = 0, column = 1)

        self.P2Frame.rowconfigure(0, weight=1)
        self.P2Frame.rowconfigure(1, weight=1)
        self.P2Frame.columnconfigure(0, weight=1)
        self.P2Frame.columnconfigure(1, weight=1)

        #Add the widgets for the logFrame
        ttk.Label(self.LogFrame, text = 'Game Log').pack()
        self.log = Text(self.LogFrame, width = 30, height = 5, wrap = 'word')
        self.log.insert('1.0', 'Game Log will be shown here:\n')
        self.log.config(state = 'disabled')
        self.log.pack()



        #Add the widgets for the buttonFrame
        self.surrenderButton = ttk.Button(self.buttonsFrame, text = 'Surrender', padding = 5, command = self.surrenderCommand)
        self.exitButton = ttk.Button(self.buttonsFrame, text = 'Exit', padding = 5, command = master.destroy)
        self.surrenderButton.grid(row = 0, column = 0)
        self.exitButton.grid(row = 1, column = 0)

        self.buttonsFrame.rowconfigure(0, weight = 1)
        self.buttonsFrame.rowconfigure(1, weight = 1)
        self.buttonsFrame.columnconfigure(0, weight = 1)

        #Add the chess board (8x8 board) need 64 buttons
        #Row's go from 0 to 7 and columns go from A to H

        #Adding new Style for button
        self.style.theme_use('classic')
        self.style.configure('White.TButton', background = 'blanchedalmond')
        self.style.configure('Black.TButton', background = 'gray30', foreground = 'white')
        self.style.configure('Moveable.TButton', background = 'aquamarine1', foreground = 'black')

        self.style.map('White.TButton', background = [('hover', 'slate gray'),('disabled', 'wheat3')], foreground = [('hover', 'black')])
        self.style.map('Black.TButton', background = [('hover', 'slate gray'),('disabled', 'wheat4')], foreground = [('hover', 'black')])
        self.style.map('Moveable.TButton', background = [('hover', 'aquamarine4')], foreground = [('hover', 'black')])
        
        self.A0 = ttk.Button(self.CBFrame, text = '0_0_white_rook', style = 'Black.TButton', command = lambda: self.buttonCommand(self.A0))
        self.A1 = ttk.Button(self.CBFrame, text = '0_1_white_knight', style = 'White.TButton', command = lambda: self.buttonCommand(self.A1))
        self.A2 = ttk.Button(self.CBFrame, text = '0_2_white_bishop', style = 'Black.TButton', command = lambda: self.buttonCommand(self.A2))
        self.A3 = ttk.Button(self.CBFrame, text = '0_3_white_king', style = 'White.TButton', command = lambda: self.buttonCommand(self.A3))
        self.A4 = ttk.Button(self.CBFrame, text = '0_4_white_queen', style = 'Black.TButton', command = lambda: self.buttonCommand(self.A4))
        self.A5 = ttk.Button(self.CBFrame, text = '0_5_white_bishop', style = 'White.TButton', command = lambda: self.buttonCommand(self.A5))
        self.A6 = ttk.Button(self.CBFrame, text = '0_6_white_knight', style = 'Black.TButton', command = lambda: self.buttonCommand(self.A6))
        self.A7 = ttk.Button(self.CBFrame, text = '0_7_white_rook', style = 'White.TButton', command = lambda: self.buttonCommand(self.A7))

        self.B0 = ttk.Button(self.CBFrame, text = '1_0_white_pawn', style = 'White.TButton', command = lambda: self.buttonCommand(self.B0))
        self.B1 = ttk.Button(self.CBFrame, text = '1_1_white_pawn', style = 'Black.TButton', command = lambda: self.buttonCommand(self.B1))
        self.B2 = ttk.Button(self.CBFrame, text = '1_2_white_pawn', style = 'White.TButton', command = lambda: self.buttonCommand(self.B2))
        self.B3 = ttk.Button(self.CBFrame, text = '1_3_white_pawn', style = 'Black.TButton', command = lambda: self.buttonCommand(self.B3))
        self.B4 = ttk.Button(self.CBFrame, text = '1_4_white_pawn', style = 'White.TButton', command = lambda: self.buttonCommand(self.B4))
        self.B5 = ttk.Button(self.CBFrame, text = '1_5_white_pawn', style = 'Black.TButton', command = lambda: self.buttonCommand(self.B5))
        self.B6 = ttk.Button(self.CBFrame, text = '1_6_white_pawn', style = 'White.TButton', command = lambda: self.buttonCommand(self.B6))
        self.B7 = ttk.Button(self.CBFrame, text = '1_7_white_pawn', style = 'Black.TButton', command = lambda: self.buttonCommand(self.B7))

        self.C0 = ttk.Button(self.CBFrame, text = '2_0_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.C0))
        self.C1 = ttk.Button(self.CBFrame, text = '2_1_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.C1))
        self.C2 = ttk.Button(self.CBFrame, text = '2_2_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.C2))
        self.C3 = ttk.Button(self.CBFrame, text = '2_3_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.C3))
        self.C4 = ttk.Button(self.CBFrame, text = '2_4_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.C4))
        self.C5 = ttk.Button(self.CBFrame, text = '2_5_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.C5))
        self.C6 = ttk.Button(self.CBFrame, text = '2_6_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.C6))
        self.C7 = ttk.Button(self.CBFrame, text = '2_7_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.C7))

        self.D0 = ttk.Button(self.CBFrame, text = '3_0_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.D0))
        self.D1 = ttk.Button(self.CBFrame, text = '3_1_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.D1))
        self.D2 = ttk.Button(self.CBFrame, text = '3_2_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.D2))
        self.D3 = ttk.Button(self.CBFrame, text = '3_3_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.D3))
        self.D4 = ttk.Button(self.CBFrame, text = '3_4_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.D4))
        self.D5 = ttk.Button(self.CBFrame, text = '3_5_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.D5))
        self.D6 = ttk.Button(self.CBFrame, text = '3_6_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.D6))
        self.D7 = ttk.Button(self.CBFrame, text = '3_7_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.D7))

        self.E0 = ttk.Button(self.CBFrame, text = '4_0_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.E0))
        self.E1 = ttk.Button(self.CBFrame, text = '4_1_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.E1))
        self.E2 = ttk.Button(self.CBFrame, text = '4_2_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.E2))
        self.E3 = ttk.Button(self.CBFrame, text = '4_3_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.E3))
        self.E4 = ttk.Button(self.CBFrame, text = '4_4_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.E4))
        self.E5 = ttk.Button(self.CBFrame, text = '4_5_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.E5))
        self.E6 = ttk.Button(self.CBFrame, text = '4_6_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.E6))
        self.E7 = ttk.Button(self.CBFrame, text = '4_7_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.E7))

        self.F0 = ttk.Button(self.CBFrame, text = '5_0_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.F0))
        self.F1 = ttk.Button(self.CBFrame, text = '5_1_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.F1))
        self.F2 = ttk.Button(self.CBFrame, text = '5_2_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.F2))
        self.F3 = ttk.Button(self.CBFrame, text = '5_3_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.F3))
        self.F4 = ttk.Button(self.CBFrame, text = '5_4_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.F4))
        self.F5 = ttk.Button(self.CBFrame, text = '5_5_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.F5))
        self.F6 = ttk.Button(self.CBFrame, text = '5_6_na_na', style = 'White.TButton', command = lambda: self.buttonCommand(self.F6))
        self.F7 = ttk.Button(self.CBFrame, text = '5_7_na_na', style = 'Black.TButton', command = lambda: self.buttonCommand(self.F7))

        self.G0 = ttk.Button(self.CBFrame, text = '6_0_black_pawn', style = 'Black.TButton', command = lambda: self.buttonCommand(self.G0))
        self.G1 = ttk.Button(self.CBFrame, text = '6_1_black_pawn', style = 'White.TButton', command = lambda: self.buttonCommand(self.G1))
        self.G2 = ttk.Button(self.CBFrame, text = '6_2_black_pawn', style = 'Black.TButton', command = lambda: self.buttonCommand(self.G2))
        self.G3 = ttk.Button(self.CBFrame, text = '6_3_black_pawn', style = 'White.TButton', command = lambda: self.buttonCommand(self.G3))
        self.G4 = ttk.Button(self.CBFrame, text = '6_4_black_pawn', style = 'Black.TButton', command = lambda: self.buttonCommand(self.G4))
        self.G5 = ttk.Button(self.CBFrame, text = '6_5_black_pawn', style = 'White.TButton', command = lambda: self.buttonCommand(self.G5))
        self.G6 = ttk.Button(self.CBFrame, text = '6_6_black_pawn', style = 'Black.TButton', command = lambda: self.buttonCommand(self.G6))
        self.G7 = ttk.Button(self.CBFrame, text = '6_7_black_pawn', style = 'White.TButton', command = lambda: self.buttonCommand(self.G7))

        self.H0 = ttk.Button(self.CBFrame, text = '7_0_black_rook', style = 'White.TButton', command = lambda: self.buttonCommand(self.H0))
        self.H1 = ttk.Button(self.CBFrame, text = '7_1_black_knight', style = 'Black.TButton', command = lambda: self.buttonCommand(self.H1))
        self.H2 = ttk.Button(self.CBFrame, text = '7_2_black_bishop', style = 'White.TButton', command = lambda: self.buttonCommand(self.H2))
        self.H3 = ttk.Button(self.CBFrame, text = '7_3_black_king', style = 'Black.TButton', command = lambda: self.buttonCommand(self.H3))
        self.H4 = ttk.Button(self.CBFrame, text = '7_4_black_queen', style = 'White.TButton', command = lambda: self.buttonCommand(self.H4))
        self.H5 = ttk.Button(self.CBFrame, text = '7_5_black_bishop', style = 'Black.TButton', command = lambda: self.buttonCommand(self.H5))
        self.H6 = ttk.Button(self.CBFrame, text = '7_6_black_knight', style = 'White.TButton', command = lambda: self.buttonCommand(self.H6))
        self.H7 = ttk.Button(self.CBFrame, text = '7_7_black_rook', style = 'Black.TButton', command = lambda: self.buttonCommand(self.H7))

        #Keep track of the loaction of the king
        ChessGame.P1KING = self.A3
        ChessGame.P2KING = self.H3

        #Display the buttons on Frame
        self.A0.grid(row = 0, column = 0)
        self.A1.grid(row = 1, column = 0)
        self.A2.grid(row = 2, column = 0)
        self.A3.grid(row = 3, column = 0)
        self.A4.grid(row = 4, column = 0)
        self.A5.grid(row = 5, column = 0)
        self.A6.grid(row = 6, column = 0)
        self.A7.grid(row = 7, column = 0)

        self.B0.grid(row = 0, column = 1)
        self.B1.grid(row = 1, column = 1)
        self.B2.grid(row = 2, column = 1)
        self.B3.grid(row = 3, column = 1)
        self.B4.grid(row = 4, column = 1)
        self.B5.grid(row = 5, column = 1)
        self.B6.grid(row = 6, column = 1)
        self.B7.grid(row = 7, column = 1)

        self.C0.grid(row = 0, column = 2)
        self.C1.grid(row = 1, column = 2)
        self.C2.grid(row = 2, column = 2)
        self.C3.grid(row = 3, column = 2)
        self.C4.grid(row = 4, column = 2)
        self.C5.grid(row = 5, column = 2)
        self.C6.grid(row = 6, column = 2)
        self.C7.grid(row = 7, column = 2)

        self.D0.grid(row = 0, column = 3)
        self.D1.grid(row = 1, column = 3)
        self.D2.grid(row = 2, column = 3)
        self.D3.grid(row = 3, column = 3)
        self.D4.grid(row = 4, column = 3)
        self.D5.grid(row = 5, column = 3)
        self.D6.grid(row = 6, column = 3)
        self.D7.grid(row = 7, column = 3)

        self.E0.grid(row = 0, column = 4)
        self.E1.grid(row = 1, column = 4)
        self.E2.grid(row = 2, column = 4)
        self.E3.grid(row = 3, column = 4)
        self.E4.grid(row = 4, column = 4)
        self.E5.grid(row = 5, column = 4)
        self.E6.grid(row = 6, column = 4)
        self.E7.grid(row = 7, column = 4)

        self.F0.grid(row = 0, column = 5)
        self.F1.grid(row = 1, column = 5)
        self.F2.grid(row = 2, column = 5)
        self.F3.grid(row = 3, column = 5)
        self.F4.grid(row = 4, column = 5)
        self.F5.grid(row = 5, column = 5)
        self.F6.grid(row = 6, column = 5)
        self.F7.grid(row = 7, column = 5)

        self.G0.grid(row = 0, column = 6)
        self.G1.grid(row = 1, column = 6)
        self.G2.grid(row = 2, column = 6)
        self.G3.grid(row = 3, column = 6)
        self.G4.grid(row = 4, column = 6)
        self.G5.grid(row = 5, column = 6)
        self.G6.grid(row = 6, column = 6)
        self.G7.grid(row = 7, column = 6)
        
        self.H0.grid(row = 0, column = 7)
        self.H1.grid(row = 1, column = 7)
        self.H2.grid(row = 2, column = 7)
        self.H3.grid(row = 3, column = 7)
        self.H4.grid(row = 4, column = 7)
        self.H5.grid(row = 5, column = 7)
        self.H6.grid(row = 6, column = 7)
        self.H7.grid(row = 7, column = 7)

        self.CBFrame.rowconfigure(0, weight = 1)
        self.CBFrame.rowconfigure(1, weight = 1)
        self.CBFrame.rowconfigure(2, weight = 1)
        self.CBFrame.rowconfigure(3, weight = 1)
        self.CBFrame.rowconfigure(4, weight = 1)
        self.CBFrame.rowconfigure(5, weight = 1)
        self.CBFrame.rowconfigure(6, weight = 1)
        self.CBFrame.rowconfigure(7, weight = 1)

        self.CBFrame.columnconfigure(0, weight = 1)
        self.CBFrame.columnconfigure(1, weight = 1)
        self.CBFrame.columnconfigure(2, weight = 1)
        self.CBFrame.columnconfigure(3, weight = 1)
        self.CBFrame.columnconfigure(4, weight = 1)
        self.CBFrame.columnconfigure(5, weight = 1)
        self.CBFrame.columnconfigure(6, weight = 1)
        self.CBFrame.columnconfigure(7, weight = 1)

    def centralButtonCommand(self, playerButton):
        p1ButtonList = [[self.P1BlackB, 1], [self.P1WhiteB, 2], [self.P1GreenB, 3], [self.P1RedB, 4], [self.P1GoldB, 5]]
        p2ButtonList = [[self.P2BlackB, 1], [self.P2WhiteB, 2], [self.P2GreenB, 3], [self.P2RedB, 4], [self.P2GoldB, 5]]
        
        if(playerButton == self.P1BlackB):
            if(self.P2BlackB.state() == () and ChessGame.P2Color == ""):#means this player is picking color
                self.P1WhiteB.state(['disabled'])
                self.P1GreenB.state(['disabled'])
                self.P1RedB.state(['disabled'])
                self.P1GoldB.state(['disabled'])
                self.P2BlackB.state(['disabled'])
                ChessGame.P1Color = 'black'
            elif(self.P2BlackB.state() != () and ChessGame.P1Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p1ButtonList:
                    if(button[0] == self.P1BlackB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P1Color = 'black'
            elif(self.P2BlackB.state() != () and ChessGame.P2Color == ""):#means nemy player has not picked a color and this player is deselecting this color
                for button in p1ButtonList:
                    button[0].state(['!disabled'])
                self.P2BlackB.state(['!disabled'])
                ChessGame.P1Color = ""
            elif(self.P2BlackB.state() != () and ChessGame.P1Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p2ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p1ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P1Color = ""
                    
        elif(playerButton == self.P2BlackB):
            if(self.P1BlackB.state() == () and ChessGame.P1Color == ""):#means this player is picking color
                self.P2WhiteB.state(['disabled'])
                self.P2GreenB.state(['disabled'])
                self.P2RedB.state(['disabled'])
                self.P2GoldB.state(['disabled'])
                self.P1BlackB.state(['disabled'])
                ChessGame.P2Color = 'black'
            elif(self.P1BlackB.state() != () and ChessGame.P2Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p2ButtonList:
                    if(button[0] == self.P2BlackB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P2Color = 'black'
            elif(self.P1BlackB.state() != () and ChessGame.P1Color == ""):#means enemy player has not picked a color and this player is deselecting this color
                for button in p2ButtonList:
                    button[0].state(['!disabled'])
                self.P1BlackB.state(['!disabled'])
                ChessGame.P2Color = ""
            elif(self.P1BlackB.state() != () and ChessGame.P2Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p1ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p2ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P2Color = ""
        elif(playerButton == self.P1WhiteB):
            if(self.P2WhiteB.state() == () and ChessGame.P2Color == ""):#means this player is picking color
                self.P2WhiteB.state(['disabled'])
                self.P1GreenB.state(['disabled'])
                self.P1RedB.state(['disabled'])
                self.P1GoldB.state(['disabled'])
                self.P1BlackB.state(['disabled'])
                ChessGame.P1Color = 'white'
            elif(self.P2WhiteB.state() != () and ChessGame.P1Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p1ButtonList:
                    if(button[0] == self.P1WhiteB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P1Color = 'white'
            elif(self.P2WhiteB.state() != () and ChessGame.P2Color == ""):#means enemy player has not picked a color and this player is deselecting this color
                for button in p1ButtonList:
                    button[0].state(['!disabled'])
                self.P2WhiteB.state(['!disabled'])
                ChessGame.P1Color = ""
            elif(self.P2WhiteB.state() != () and ChessGame.P1Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p2ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p1ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P1Color = ""
        elif(playerButton == self.P2WhiteB):
            if(self.P1WhiteB.state() == () and ChessGame.P1Color == ""):#means this player is picking color
                self.P1WhiteB.state(['disabled'])
                self.P2GreenB.state(['disabled'])
                self.P2RedB.state(['disabled'])
                self.P2GoldB.state(['disabled'])
                self.P2BlackB.state(['disabled'])
                ChessGame.P2Color = 'white'
            elif(self.P1WhiteB.state() != () and ChessGame.P2Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p2ButtonList:
                    if(button[0] == self.P2WhiteB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P2Color = 'white'
            elif(self.P1WhiteB.state() != () and ChessGame.P1Color == ""):#means enemy player has not picked a color and this player is deselecting this color
                for button in p2ButtonList:
                    button[0].state(['!disabled'])
                self.P1WhiteB.state(['!disabled'])
                ChessGame.P2Color = ""
            elif(self.P1WhiteB.state() != () and ChessGame.P2Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p1ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p2ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P2Color = ""
        elif(playerButton == self.P1GreenB):
            if(self.P2GreenB.state() == () and ChessGame.P2Color == ""):#means this player is picking color
                self.P1WhiteB.state(['disabled'])
                self.P2GreenB.state(['disabled'])
                self.P1RedB.state(['disabled'])
                self.P1GoldB.state(['disabled'])
                self.P1BlackB.state(['disabled'])
                ChessGame.P1Color = 'green'
            elif(self.P2GreenB.state() != () and ChessGame.P1Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p1ButtonList:
                    if(button[0] == self.P1GreenB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P1Color = 'green'
            elif(self.P2GreenB.state() != () and ChessGame.P2Color == ""):#means enemy player has not picked a color and this player is deselecting this color
                for button in p1ButtonList:
                    button[0].state(['!disabled'])
                self.P2GreenB.state(['!disabled'])
                ChessGame.P1Color = ""
            elif(self.P2GreenB.state() != () and ChessGame.P1Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p2ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p1ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P1Color = ""
        elif(playerButton == self.P2GreenB):
            if(self.P1GreenB.state() == () and ChessGame.P1Color == ""):#means this player is picking color
                self.P2WhiteB.state(['disabled'])
                self.P1GreenB.state(['disabled'])
                self.P2RedB.state(['disabled'])
                self.P2GoldB.state(['disabled'])
                self.P2BlackB.state(['disabled'])
                ChessGame.P2Color = 'green'
            elif(self.P1GreenB.state() != () and ChessGame.P2Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p2ButtonList:
                    if(button[0] == self.P2GreenB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P2Color = 'green'
            elif(self.P1GreenB.state() != () and ChessGame.P1Color == ""):#means enemy player has not picked a color and this player is deselecting this color
                for button in p2ButtonList:
                    button[0].state(['!disabled'])
                self.P1GreenB.state(['!disabled'])
                ChessGame.P2Color = ""
            elif(self.P1GreenB.state() != () and ChessGame.P2Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p1ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p2ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P2Color = ""
        elif(playerButton == self.P1RedB):
            if(self.P2RedB.state() == () and ChessGame.P2Color == ""):#means this player is picking color
                self.P1WhiteB.state(['disabled'])
                self.P1GreenB.state(['disabled'])
                self.P2RedB.state(['disabled'])
                self.P1GoldB.state(['disabled'])
                self.P1BlackB.state(['disabled'])
                ChessGame.P1Color = 'red'
            elif(self.P2RedB.state() != () and ChessGame.P1Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p1ButtonList:
                    if(button[0] == self.P1RedB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P1Color = 'red'
            elif(self.P2RedB.state() != () and ChessGame.P2Color == ""):#means enemy player has not picked a color and this player is deselecting this color
                for button in p1ButtonList:
                    button[0].state(['!disabled'])
                self.P2RedB.state(['!disabled'])
                ChessGame.P1Color = ""
            elif(self.P2RedB.state() != () and ChessGame.P1Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p2ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p1ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P1Color = ""
        elif(playerButton == self.P2RedB):
            if(self.P1RedB.state() == () and ChessGame.P1Color == ""):#means this player is picking color
                self.P2WhiteB.state(['disabled'])
                self.P2GreenB.state(['disabled'])
                self.P1RedB.state(['disabled'])
                self.P2GoldB.state(['disabled'])
                self.P2BlackB.state(['disabled'])
                ChessGame.P2Color = 'red'
            elif(self.P1RedB.state() != () and ChessGame.P2Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p2ButtonList:
                    if(button[0] == self.P2RedB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P2Color = 'red'
            elif(self.P1RedB.state() != () and ChessGame.P1Color == ""):#means enemy player has not picked a color and this player is deselecting this color
                for button in p2ButtonList:
                    button[0].state(['!disabled'])
                self.P1RedB.state(['!disabled'])
                ChessGame.P2Color = ""
            elif(self.P1RedB.state() != () and ChessGame.P2Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p1ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p2ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P2Color = ""
        elif(playerButton == self.P1GoldB):
            if(self.P2GoldB.state() == () and ChessGame.P2Color == ""):#means this player is picking color
                self.P1WhiteB.state(['disabled'])
                self.P1GreenB.state(['disabled'])
                self.P1RedB.state(['disabled'])
                self.P2GoldB.state(['disabled'])
                self.P1BlackB.state(['disabled'])
                ChessGame.P1Color = 'gold'
            elif(self.P2GoldB.state() != () and ChessGame.P1Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p1ButtonList:
                    if(button[0] == self.P1GoldB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P1Color = 'gold'
            elif(self.P2GoldB.state() != () and ChessGame.P2Color == ""):#means enemy player has not picked a color and this player is deselecting this color
                for button in p1ButtonList:
                    button[0].state(['!disabled'])
                self.P2GoldB.state(['!disabled'])
                ChessGame.P1Color = ""
            elif(self.P2GoldB.state() != () and ChessGame.P1Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p2ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p1ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P1Color = ""
        elif(playerButton == self.P2GoldB):
            if(self.P1GoldB.state() == () and ChessGame.P1Color == ""):#means this player is picking color
                self.P2WhiteB.state(['disabled'])
                self.P2GreenB.state(['disabled'])
                self.P2RedB.state(['disabled'])
                self.P1GoldB.state(['disabled'])
                self.P2BlackB.state(['disabled'])
                ChessGame.P2Color = 'gold'
            elif(self.P1GoldB.state() != () and ChessGame.P2Color == ""):#means enemy player already picked a color and this Player is picking color
                for button in p2ButtonList:
                    if(button[0] == self.P2GoldB):
                        pass
                    else:
                        button[0].state(['disabled'])
                ChessGame.P2Color = 'gold'
            elif(self.P1GoldB.state() != () and ChessGame.P1Color == ""):#means enemy player has not picked a color and this player is deselecting this color
                for button in p2ButtonList:
                    button[0].state(['!disabled'])
                self.P1GoldB.state(['!disabled'])
                ChessGame.P2Color = ""
            elif(self.P1GoldB.state() != () and ChessGame.P2Color != ""):#means enemy player has picked a color and this player is deselecting this color
                buttonId = None
                for button in p1ButtonList:
                    if(button[0].state() == ()):
                        buttonId = button[1]
                for button in p2ButtonList:
                    if(button[1] == buttonId):
                        pass
                    else:
                        button[0].state(['!disabled'])

                ChessGame.P2Color = ""

    def submit(self):
        ChessGame.P1Pass = self.P1PasswordValue.get()
        ChessGame.P2Pass = self.P2PasswordValue.get()
        ChessGame.P1UserName = self.P1UserName.get()
        ChessGame.P2UserName = self.P2UserName.get()
        if(ChessGame.P1Color == "" or ChessGame.P2Color == ""):
            messagebox.showerror(title = "Required Color", message = "One or more player has not selected a COLOR to play as,\nPlease do so to move forward, Thank You!!!")
        elif (ChessGame.P1UserName == "" or ChessGame.P2UserName == ""):
            messagebox.showerror(title = "Required Username", message = "One or more player has not inserted USERNAME\nPlease do so to move forward, Thank You!!!")
        elif (ChessGame.P1Pass == "" or ChessGame.P2Pass == ""):
            messagebox.showerror(title = "Required Password", message = "One or more player has not inserted PASSWORD\nPlease do so to move forward, Thank You!!!")
        else:

    
            ChessGame.P1Pass = self.P1PasswordValue.get()
            ChessGame.P2Pass = self.P2PasswordValue.get()

            self.P1PasswordValue.delete(0, END)
            self.P2PasswordValue.delete(0, END)

            messagebox.showinfo(title = "Rerouting", message = "Rerouting to the game page, hold tight!!!")

            self.notebook.insert(END, self.gamePage, text = 'Game Page')
            self.notebook.tab(0, state = "hidden")

            self.GPHeaderTitle.config(text = "Lets Start, {}'s Turn".format(ChessGame.P1UserName))
            self.P1Hist.insert('1.0', "{}'s History:\n".format(ChessGame.P1UserName))
            self.P1Hist.insert(END, "King\n")
            self.P1Hist.insert(END, "Queen X1\n")
            self.P1Hist.insert(END, "Bishop X2\n")
            self.P1Hist.insert(END, "Knight X2\n")
            self.P1Hist.insert(END, "Rook X2\n")
            self.P1Hist.insert(END, "Pawn X8\n")
            self.P1Hist.config(state = 'disabled')
            self.P2Hist.insert('1.0', "{}'s History:\n".format(ChessGame.P2UserName))
            self.P2Hist.insert(END, "King\n")
            self.P2Hist.insert(END, "Queen X1\n")
            self.P2Hist.insert(END, "Bishop X2\n")
            self.P2Hist.insert(END, "Knight X2\n")
            self.P2Hist.insert(END, "Rook X2\n")
            self.P2Hist.insert(END, "Pawn X8\n")
            self.P2Hist.config(state = 'disabled')
            ttk.Label(self.P1Frame, text = '{}'.format(ChessGame.P1UserName)).grid(row = 0, column = 0)
            ttk.Label(self.P2Frame, text = '{}'.format(ChessGame.P2UserName)).grid(row = 0, column = 0)

            #Create the chess map in the background 
            self.addImages()
            self.createMap()
            self.fixBoard()
            #self.notebook.forget(0)


    def createMap(self): 
        ChessGame.state = GameState.WAIT1
        self.chessMap = [[self.A0, self.A1, self.A2, self.A3, self.A4, self.A5, self.A6, self.A7],
                    [self.B0, self.B1, self.B2, self.B3, self.B4, self.B5, self.B6, self.B7],
                    [self.C0, self.C1, self.C2, self.C3, self.C4, self.C5, self.C6, self.C7],
                    [self.D0, self.D1, self.D2, self.D3, self.D4, self.D5, self.D6, self.D7],
                    [self.E0, self.E1, self.E2, self.E3, self.E4, self.E5, self.E6, self.E7],
                    [self.F0, self.F1, self.F2, self.F3, self.F4, self.F5, self.F6, self.F7],
                    [self.G0, self.G1, self.G2, self.G3, self.G4, self.G5, self.G6, self.G7],
                    [self.H0, self.H1, self.H2, self.H3, self.H4, self.H5, self.H6, self.H7]]
        self.playerTurn(1)

    def buttonCommand(self, buttonClicked):
        x,y,color,piece = buttonClicked.cget('text').split('_')
        x = int(x)
        y = int(y)
        if(ChessGame.pieceToMove != None):
            oldx, oldy, oldColor, oldPiece = ChessGame.pieceToMove.cget('text').split('_')
        else:
            oldx = None
            oldy = None
            oldColor = None
            oldPiece = None

        if(piece == "pawn" or (oldPiece == 'pawn' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_pawn_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_pawn_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.PLANMOVE2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(2)
                    ChessGame.state = GameState.WAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.INCHECKPLAN2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(2)
                    ChessGame.state = GameState.INCHECKWAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            

        elif(piece == "rook" or (oldPiece == 'rook' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_rook_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_rook_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.PLANMOVE2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(2)
                    ChessGame.state = GameState.WAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.INCHECKPLAN2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(2)
                    ChessGame.state = GameState.INCHECKWAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            
        elif(piece == "knight" or (oldPiece == 'knight' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_knight_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_knight_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.PLANMOVE2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(2)
                    ChessGame.state = GameState.WAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.INCHECKPLAN2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(2)
                    ChessGame.state = GameState.INCHECKWAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)


        elif(piece == "bishop" or (oldPiece == 'bishop' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_bishop_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_bishop_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.PLANMOVE2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(2)
                    ChessGame.state = GameState.WAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.INCHECKPLAN2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(2)
                    ChessGame.state = GameState.INCHECKWAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)

        elif(piece == "queen" or (oldPiece == 'queen' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_queen_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_queen_move(x, y, color)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.PLANMOVE2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(2)
                    ChessGame.state = GameState.WAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.INCHECKPLAN2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(2)
                    ChessGame.state = GameState.INCHECKWAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)

            
        elif(piece == "king" or (oldPiece == 'king' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_king_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_king_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.PLANMOVE2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(2)
                    ChessGame.state = GameState.WAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                listToEnable = self.limitingMovement(color, listToEnable, piece, x, y)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        if(self.checkStalemate('black') == False):
                            ChessGame.state = GameState.WAIT2
                            self.playerTurn(2)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT2
                        self.checkPlayerTurn(2)
            elif(ChessGame.state == GameState.INCHECKPLAN2):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(2)
                    ChessGame.state = GameState.INCHECKWAIT2
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('white')
                    if(not check):
                        if(self.checkStalemate('white') == False):
                            ChessGame.state = GameState.WAIT1
                            self.playerTurn(1)
                        else:
                            self.endGame('stalemate')
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)


        
    def plan_pawn_move(self, x, y, color, checkCall = False):
        listToEnable = [[x,y]]

        if(color == 'white'):  
            if( x+1 <= 7):
                newx, newy, newColor, newPiece = self.chessMap[x+1][y].cget('text').split('_')
                if(newColor == 'na'):
                    listToEnable.append([x+1,y])
                if(y-1 >= 0):
                    newx, newy, newColor, newPiece = self.chessMap[x+1][y-1].cget('text').split('_')
                    if(newColor == 'black'):
                        listToEnable.append([x+1,y-1])
                if(y+1 <= 7):
                    newx, newy, newColor, newPiece = self.chessMap[x+1][y+1].cget('text').split('_')
                    if(newColor == 'black'):
                        listToEnable.append([x+1,y+1])
                if(x == 1 and ([x+1,y] in listToEnable)):
                    newx, newy, newColor, newPiece = self.chessMap[x+2][y].cget('text').split('_')
                    if(newColor == 'na'):
                        listToEnable.append([x+2,y])
        elif(color == 'black'):  
            if( x-1 >= 0):
                newx, newy, newColor, newPiece = self.chessMap[x-1][y].cget('text').split('_')
                if(newColor == 'na'):
                    listToEnable.append([x-1,y])
                if(y-1 >= 0):
                    newx, newy, newColor, newPiece = self.chessMap[x-1][y-1].cget('text').split('_')
                    if(newColor == 'white'):
                        listToEnable.append([x-1,y-1])
                if(y+1 <= 7):
                    newx, newy, newColor, newPiece = self.chessMap[x-1][y+1].cget('text').split('_')
                    if(newColor == 'white'):
                        listToEnable.append([x-1,y+1])
                if(x == 6):
                    newx, newy, newColor, newPiece = self.chessMap[x-2][y].cget('text').split('_')
                    if(newColor == 'na'and ([x-1,y] in listToEnable)):
                        listToEnable.append([x-2,y])   
        return listToEnable




    def plan_rook_move(self, x, y, color, kingCall = False, checkCall = False):#4 possible paths which are straight in all directions
        
        if(checkCall == False):
            listToEnable = [[x,y]]
        
            #Path 1 - Going up
            for i in range(y):#can only go up as much as it is currently for example if in the 4th row it can only move up 4 times (due to 0 indexing)
                newx, newy, newColor, newPiece = self.chessMap[x][y-(i+1)].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                if(newColor == 'na'):
                    listToEnable.append([x,y-(i+1)])
                elif(newColor != color):
                    listToEnable.append([x,y-(i+1)])
                    break
                elif(newColor == color and kingCall == True):
                    listToEnable.append([x,y-(i+1)])
                    break
                elif(newColor == color and kingCall == False):
                    break
            #path 2 - Going down
            for i in range(7-y):#Going down
                newx, newy, newColor, newPiece = self.chessMap[x][y+(i+1)].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                if(newColor == 'na'):
                    listToEnable.append([x,y+(i+1)])
                elif(newColor != color):
                    listToEnable.append([x,y+(i+1)])
                    break
                elif(newColor == color and kingCall == True):
                    listToEnable.append([x,y+(i+1)])
                    break
                elif(newColor == color and kingCall == False):
                    break
            #Path 3 - Going Left
            for i in range(x):#can only go left as much as it is currently for example if in the 4th column it can only move left 4 times (due to 0 indexing)
                newx, newy, newColor, newPiece = self.chessMap[x-(i+1)][y].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                if(newColor == 'na'):
                    listToEnable.append([x-(i+1),y])
                elif(newColor != color):
                    listToEnable.append([x-(i+1),y])
                    break
                elif(newColor == color and kingCall == True):
                    listToEnable.append([x-(i+1),y])
                    break
                elif(newColor == color and kingCall == False):
                    break
            #Path 4 - Going Right
            for i in range(7-x):#Going right
                newx, newy, newColor, newPiece = self.chessMap[x+(i+1)][y].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                if(newColor == 'na'):
                    listToEnable.append([x+(i+1),y])
                elif(newColor != color):
                    listToEnable.append([x+(i+1),y])
                    break
                elif(newColor == color and kingCall == True):
                    listToEnable.append([x+(i+1),y])
                    break
                elif(newColor == color and kingCall == False):
                    break

            return listToEnable
        elif(checkCall == True):
            futAttackLocations = [[x,y]]
            
            #Path 1 - Going up
            piece = 0
            pieceInQuestion = None
            for i in range(y):#can only go up as much as it is currently for example if in the 4th row it can only move up 4 times (due to 0 indexing)
                newx, newy, newColor, newPiece = self.chessMap[x][y-(i+1)].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                if(newColor == 'na'):
                    futAttackLocations.append([x,y-(i+1)])
                elif(newColor != color):
                    if(piece == 0):
                        pieceInQuestion = [int(newx), int(newy), newPiece]
                        futAttackLocations.append([x,y-(i+1)])
                        piece += 1
                    elif(piece == 1 and newPiece == 'king'):
                        return [pieceInQuestion, futAttackLocations]
                    elif(piece == 1 and newPiece != 'king'):
                        break
                elif(newColor == color and kingCall == True):
                    futAttackLocations.append([x,y-(i+1)])
                    break
                elif(newColor == color and kingCall == False):
                    break
            futAttackLocations = [[x,y]]

            #path 2 - Going down
            piece = 0
            pieceInQuestion = None
            for i in range(7-y):#Going down
                newx, newy, newColor, newPiece = self.chessMap[x][y+(i+1)].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                if(newColor == 'na'):
                    futAttackLocations.append([x,y+(i+1)])
                elif(newColor != color):
                    if(piece == 0):
                        pieceInQuestion = [int(newx), int(newy), newPiece]
                        futAttackLocations.append([x,y+(i+1)])
                        piece += 1
                    elif(piece == 1 and newPiece == 'king'):
                        return [pieceInQuestion, futAttackLocations]
                    elif(piece == 1 and newPiece != 'king'):
                        break
                elif(newColor == color and kingCall == True):
                    futAttackLocations.append([x,y+(i+1)])
                    break
                elif(newColor == color and kingCall == False):
                    break
            futAttackLocations = [[x,y]]

            #Path 3 - Going Left
            piece = 0
            pieceInQuestion = None
            for i in range(x):#can only go left as much as it is currently for example if in the 4th column it can only move left 4 times (due to 0 indexing)
                newx, newy, newColor, newPiece = self.chessMap[x-(i+1)][y].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                if(newColor == 'na'):
                    futAttackLocations.append([x-(i+1),y])
                elif(newColor != color):
                    if(piece == 0):
                        pieceInQuestion = [int(newx), int(newy), newPiece]
                        futAttackLocations.append([x-(i+1),y])
                        piece += 1
                    elif(piece == 1 and newPiece == 'king'):
                        return [pieceInQuestion, futAttackLocations]
                    elif(piece == 1 and newPiece != 'king'):
                        break
                elif(newColor == color and kingCall == True):
                    futAttackLocations.append([x-(i+1),y])
                    break
                elif(newColor == color and kingCall == False):
                    break
            futAttackLocations = [[x,y]]

            #Path 4 - Going Right
            piece = 0
            pieceInQuestion = None
            for i in range(7-x):#Going right
                newx, newy, newColor, newPiece = self.chessMap[x+(i+1)][y].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                if(newColor == 'na'):
                    futAttackLocations.append([x+(i+1),y])
                elif(newColor != color):
                    if(piece == 0):
                        pieceInQuestion = [int(newx), int(newy), newPiece]
                        futAttackLocations.append([x+(i+1),y])
                        piece += 1
                    elif(piece == 1 and newPiece == 'king'):
                        return [pieceInQuestion, futAttackLocations]
                    elif(piece == 1 and newPiece != 'king'):
                        break
                elif(newColor == color and kingCall == True):
                    futAttackLocations.append([x+(i+1),y])
                    break
                elif(newColor == color and kingCall == False):
                    break

            return False




    def plan_knight_move(self, x, y, color, kingCall = False, checkCall = False):

        listToEnable = [[x,y]]
        #8 possible locations at max regardless of color - so no need for a iterative method
        if(x-1 >= 0 and y-2 >= 0):
            newx, newy, newColor, newPiece = self.chessMap[x-1][y-2].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x-1,y-2])
            if(color == newColor and kingCall == True):
                listToEnable.append([x-1,y-2])
        if(x+1 <= 7 and y-2 >= 0):
            newx, newy, newColor, newPiece = self.chessMap[x+1][y-2].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x+1,y-2])
            if(color == newColor and kingCall == True):
                listToEnable.append([x+1,y-2])
        if(x-2 >= 0 and y-1 >= 0):
            newx, newy, newColor, newPiece = self.chessMap[x-2][y-1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x-2,y-1])
            if(color == newColor and kingCall == True):
                listToEnable.append([x-2,y-1])
        if(x-2 >= 0 and y+1 <= 7):
            newx, newy, newColor, newPiece = self.chessMap[x-2][y+1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x-2,y+1])
            if(color == newColor and kingCall == True):
                listToEnable.append([x-2,y+1])
        if(x+2 <= 7 and y-1 >= 0):
            newx, newy, newColor, newPiece = self.chessMap[x+2][y-1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x+2,y-1])
            if(color == newColor and kingCall == True):
                listToEnable.append([x+2,y-1])
        if(x+2 <= 7 and y+1 <= 7):
            newx, newy, newColor, newPiece = self.chessMap[x+2][y+1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x+2,y+1])
            if(color == newColor and kingCall == True):
                listToEnable.append([x+2,y+1])
        if(x-1 >= 0 and y+2 <= 7):
            newx, newy, newColor, newPiece = self.chessMap[x-1][y+2].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x-1,y+2])
            if(color == newColor and kingCall == True):
                listToEnable.append([x-1,y+2])
        if(x+1 <= 7 and y+2 <= 7):
            newx, newy, newColor, newPiece = self.chessMap[x+1][y+2].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x+1,y+2])
            if(color == newColor and kingCall == True):
                listToEnable.append([x+1,y+2])

        return listToEnable

    def plan_bishop_move(self, x, y, color, kingCall = False, checkCall = False):
        
        if(checkCall == False):
        
            listToEnable = [[x,y]]
            
            #Path 1 - Going up and left
            for i in range(7):#Max times you can go up and to the left is 7
                if(x-(i+1) >= 0 and y-(i+1) >=0 ):
                    newx, newy, newColor, newPiece = self.chessMap[x-(i+1)][y-(i+1)].cget('text').split('_')
                    if(newColor == 'na'):
                        listToEnable.append([x-(i+1),y-(i+1)])
                    elif(newColor != color):
                        listToEnable.append([x-(i+1),y-(i+1)])
                        break
                    elif(newColor == color and kingCall == True):
                        listToEnable.append([x-(i+1),y-(i+1)])
                        break
                    elif(newColor == color and kingCall == False):
                        break
                else:
                    break
            #Path 2 - Going up and right 
            for i in range(7):#max times you can go up and right is 7
                if(x+(i+1) <= 7 and y-(i+1) >= 0):
                    newx, newy, newColor, newPiece = self.chessMap[x+(i+1)][y-(i+1)].cget('text').split('_')
                    if(newColor == 'na'):
                        listToEnable.append([x+(i+1),y-(i+1)])
                    elif(newColor != color):
                        listToEnable.append([x+(i+1),y-(i+1)])
                        break
                    elif(newColor == color and kingCall == True):
                        listToEnable.append([x+(i+1),y-(i+1)])
                        break
                    elif(newColor == color and kingCall == False):
                        break
            #Path 3 - Going down and left
            for i in range(7):#max times you can go down and left is 7
                if(x-(i+1) >= 0 and y+(i+1) <= 7):
                    newx, newy, newColor, newPiece = self.chessMap[x-(i+1)][y+(i+1)].cget('text').split('_')
                    if(newColor == 'na'):
                        listToEnable.append([x-(i+1),y+(i+1)])
                    elif(newColor != color):
                        listToEnable.append([x-(i+1),y+(i+1)])
                        break
                    elif(newColor == color and kingCall == True):
                        listToEnable.append([x-(i+1),y+(i+1)])
                        break
                    elif(newColor == color and kingCall == False):
                        break
            #Path 4 - Going down and right
            for i in range(7):#max times you can go down and right is 7
                if (x+(i+1) <= 7 and y+(i+1) <= 7):
                    newx, newy, newColor, newPiece = self.chessMap[x+(i+1)][y+(i+1)].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                    if(newColor == 'na'):
                        listToEnable.append([x+(i+1),y+(i+1)])
                    elif(newColor != color):
                        listToEnable.append([x+(i+1),y+(i+1)])
                        break
                    elif(newColor == color and kingCall == True):
                        listToEnable.append([x+(i+1),y+(i+1)])
                        break
                    elif(newColor == color and kingCall == False):
                        break

            return listToEnable
        elif(checkCall == True):
            futAttackLocations = [[x,y]]
            #Path 1 - Going up and left
            piece = 0
            pieceInQuestion = None
            for i in range(7):#Max times you can go up and to the left is 7
                if(x-(i+1) >= 0 and y-(i+1) >=0 ):
                    newx, newy, newColor, newPiece = self.chessMap[x-(i+1)][y-(i+1)].cget('text').split('_')
                    if(newColor == 'na'):
                        futAttackLocations.append([x-(i+1),y-(i+1)])
                    elif(newColor != color):
                        if(piece == 0 and newPiece != 'king'):
                            pieceInQuestion = [int(newx), int(newy), newPiece]
                            futAttackLocations.append([x-(i+1),y-(i+1)])
                            piece += 1
                        elif(piece == 1 and newPiece == 'king'):
                            return [pieceInQuestion, futAttackLocations]
                        elif(piece == 1 and newPiece != 'king'):
                            break
                    elif(newColor == color and kingCall == True):
                        futAttackLocations.append([x-(i+1),y-(i+1)])
                        break
                    elif(newColor == color and kingCall == False):
                        break
                else:
                    break
            futAttackLocations = [[x,y]]

            #Path 2 - Going up and right 
            piece = 0
            pieceInQuestion = None
            for i in range(7):#max times you can go up and right is 7
                if(x+(i+1) <= 7 and y-(i+1) >= 0):
                    newx, newy, newColor, newPiece = self.chessMap[x+(i+1)][y-(i+1)].cget('text').split('_')
                    if(newColor == 'na'):
                        futAttackLocations.append([x+(i+1),y-(i+1)])
                    elif(newColor != color):
                        if(piece == 0 and newPiece != 'king'):
                            pieceInQuestion = [int(newx), int(newy), newPiece]
                            futAttackLocations.append([x+(i+1),y-(i+1)])
                            piece += 1
                        elif(piece == 1 and newPiece == 'king'):
                            return [pieceInQuestion, futAttackLocations]
                        elif(piece == 1 and newPiece != 'king'):
                            break
                    elif(newColor == color and kingCall == True):
                        futAttackLocations.append([x+(i+1),y-(i+1)])
                        break
                    elif(newColor == color and kingCall == False):
                        break
                else:
                    break
            futAttackLocations = [[x,y]]

            #Path 3 - Going down and left
            piece = 0
            pieceInQuestion = None
            for i in range(7):#max times you can go down and left is 7
                if(x-(i+1) >= 0 and y+(i+1) <= 7):
                    newx, newy, newColor, newPiece = self.chessMap[x-(i+1)][y+(i+1)].cget('text').split('_')
                    if(newColor == 'na'):
                        futAttackLocations.append([x-(i+1),y+(i+1)])
                    elif(newColor != color):
                        if(piece == 0 and newPiece != 'king'):
                            pieceInQuestion = [int(newx), int(newy), newPiece]
                            futAttackLocations.append([x-(i+1),y+(i+1)])
                            piece += 1
                        elif(piece == 1 and newPiece == 'king'):
                            return [pieceInQuestion, futAttackLocations]
                        elif(piece == 1 and newPiece != 'king'):
                            break
                    elif(newColor == color and kingCall == True):
                        futAttackLocations.append([x-(i+1),y+(i+1)])
                        break
                    elif(newColor == color and kingCall == False):
                        break
                else:
                    break
            futAttackLocations = [[x,y]]

            #Path 4 - Going down and right
            piece = 0
            pieceInQuestion = None
            for i in range(7):#max times you can go down and right is 7
                if (x+(i+1) <= 7 and y+(i+1) <= 7):
                    newx, newy, newColor, newPiece = self.chessMap[x+(i+1)][y+(i+1)].cget('text').split('_')#the plus 1 because i starts at 0 we need it to start at 1
                    if(newColor == 'na'):
                        futAttackLocations.append([x+(i+1),y+(i+1)])
                    elif(newColor != color):
                        if(piece == 0 and newPiece != 'king'):
                            pieceInQuestion = [int(newx), int(newy), newPiece]
                            futAttackLocations.append([x+(i+1),y+(i+1)])
                            piece += 1
                        elif(piece == 1 and newPiece == 'king'):
                            return [pieceInQuestion, futAttackLocations]
                        elif(piece == 1 and newPiece != 'king'):
                            break
                    elif(newColor == color and kingCall == True):
                        futAttackLocations.append([x+(i+1),y+(i+1)])
                        break
                    elif(newColor == color and kingCall == False):
                        break
                else:
                    break

            return False


    def plan_queen_move(self, x, y, color, kingCall = False, checkCall = False):
        if(checkCall == False):
            listToEnable1 = self.plan_rook_move(x, y, color, kingCall, checkCall)
            listToEnable2 = self.plan_bishop_move(x, y, color, kingCall, checkCall)
            listToEnable2.pop(0)

            listToEnable = listToEnable1 + listToEnable2
            return listToEnable
        elif(checkCall == True):
            listToEnable1 =self.plan_rook_move(x, y, color, kingCall, checkCall)
            listToEnable2 =self.plan_bishop_move(x, y, color, kingCall, checkCall)

            if(listToEnable1 == False and listToEnable2 == False):
                listToEnable = False
            elif(listToEnable1 != False and listToEnable2 == False):
                listToEnable = listToEnable1
            elif(listToEnable1 == False and listToEnable2 != False):
                listToEnable = listToEnable2

            return listToEnable
    
    def plan_king_move(self, x, y, color):
        listToEnable = [[x,y]]
        #8 possible locations at max regardless of color - so no need for a iterative method
        if(x-1 >= 0 and y-1 >= 0):
            newx, newy, newColor, newPiece = self.chessMap[x-1][y-1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x-1,y-1])
        if(y-1 >= 0):
            newx, newy, newColor, newPiece = self.chessMap[x][y-1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x,y-1])
        if(x+1 <= 7 and y-1 >= 0):
            newx, newy, newColor, newPiece = self.chessMap[x+1][y-1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x+1,y-1])
        if(x-1 >= 0):
            newx, newy, newColor, newPiece = self.chessMap[x-1][y].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x-1,y])
        if(x+1 <= 7):
            newx, newy, newColor, newPiece = self.chessMap[x+1][y].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x+1,y])
        if(x-1 >= 0 and y+1 <= 7):
            newx, newy, newColor, newPiece = self.chessMap[x-1][y+1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x-1,y+1])
        if(y+1 <= 7):
            newx, newy, newColor, newPiece = self.chessMap[x][y+1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x,y+1])
        if(x+1 <= 7 and y+1 <= 7):
            newx, newy, newColor, newPiece = self.chessMap[x+1][y+1].cget('text').split('_')
            if(color != newColor):
                listToEnable.append([x+1,y+1])

        enemyPieces = None
        if(color == 'white'):
            enemyPieces = self.pieceFinder('black')
            squareToRemove = []
            for row in enemyPieces:
                if(row[2] == 'rook'):
                    attackPath = self.plan_rook_move(row[0], row[1], 'black', kingCall=True)
                    for square in listToEnable:
                       if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                            checkx, checky, checkColor, checkPiece = self.chessMap[int(square[0])][int(square[1])].cget('text').split('_')
                            if(checkPiece == 'rook'):
                                    squareToRemove.pop(squareToRemove.index(square))
                            if(row[1] == y and row[0] > x and ([x-1,y] in listToEnable) and square == [x+1,y] and (checkPiece == 'rook' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x-1,y])
                            if(row[1] == y and row[0] < x and ([x+1,y] in listToEnable) and square == [x-1,y] and (checkPiece == 'rook' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x+1,y])
                            if(row[0] == x and row[1] > y and ([x, y-1] in listToEnable) and square == [x,y+1] and (checkPiece == 'rook' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append(x,y-1)
                            if(row[0] == x and row[1] < y and ([x, y+1] in listToEnable) and square == [x,y-1] and (checkPiece == 'rook' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x,y+1])
                    #if the rook is in the same row or column as the king then make sure to make it so the king cannot travel backwords as that entire row is in threat
                if(row[2] == 'knight'):
                    attackPath = self.plan_knight_move(row[0], row[1], 'black', kingCall=True)
                    attackPath.pop(0)
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                if(row[2] == 'bishop'):
                    attackPath = self.plan_bishop_move(row[0], row[1], 'black', kingCall=True)
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                            checkx, checky, checkColor, checkPiece = self.chessMap[int(square[0])][int(square[1])].cget('text').split('_')
                            if(checkPiece == 'bishop'):
                                    squareToRemove.pop(squareToRemove.index(square))
                            if(x-row[0] < 0 and y-row[1] < 0 and (x-row[0] == y-row[1]) and ([x-1,y-1] in listToEnable) and square == [x+1,y+1] and (checkPiece == 'bishop' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x-1,y-1])
                            if(x-row[0] > 0 and y-row[1] > 0 and (x-row[0] == y-row[1]) and ([x+1,y+1] in listToEnable) and square == [x-1,y-1] and (checkPiece == 'bishop' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x+1,y+1])
                            if(row[0]-x > 0 and y-row[1] > 0 and (row[0]-x == y-row[1]) and ([x-1,y+1] in listToEnable) and square == [x+1,y-1] and (checkPiece == 'bishop' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x-1,y+1])
                            if(row[0]-x < 0 and y-row[1] < 0 and (row[0]-x == y-row[1]) and ([x+1,y-1] in listToEnable) and square == [x-1,y+1] and (checkPiece == 'bishop' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x+1,y-1])
                if(row[2] == 'queen'):
                    attackPath = self.plan_queen_move(row[0], row[1], 'black', kingCall=True)
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]): 
                            squareToRemove.append(square)
                            #if the queen is diagnol to the king then the entire diagnol is in threat and the king cannot go backwards on the diagnoal
                            checkx, checky, checkColor, checkPiece = self.chessMap[int(square[0])][int(square[1])].cget('text').split('_')
                            if(checkPiece == 'queen'):
                                    squareToRemove.pop(squareToRemove.index(square))
                            if(x-row[0] < 0 and y-row[1] < 0 and (x-row[0] == y-row[1]) and ([x-1,y-1] in listToEnable) and square == [x+1,y+1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):#if the queen is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x-1,y-1])
                            if(x-row[0] > 0 and y-row[1] > 0 and (x-row[0] == y-row[1]) and ([x+1,y+1] in listToEnable) and square == [x-1,y-1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):#if the queen is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x+1,y+1])
                            if(row[0]-x > 0 and y-row[1] > 0 and (row[0]-x == y-row[1]) and ([x-1,y+1] in listToEnable) and square == [x+1,y-1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):#if the queen is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x-1,y+1])
                            if(row[0]-x < 0 and y-row[1] < 0 and (row[0]-x == y-row[1]) and ([x+1,y-1] in listToEnable) and square == [x-1,y+1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):#if the queen is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x+1,y-1])
                            if(row[1] == y and row[0] > x and ([x-1,y] in listToEnable) and square == [x+1,y] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x-1,y])
                            if(row[1] == y and row[0] < x and ([x+1,y] in listToEnable) and square == [x-1,y] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x+1,y])
                            if(row[0] == x and row[1] > y and ([x, y-1] in listToEnable) and square == [x,y+1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x, y-1])
                            if(row[0] == x and row[1] < y and ([x, y+1] in listToEnable) and square == [x,y-1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x, y+1])
                if(row[2] == 'king'):
                    enemyKingPath = [row[0],row[1]]
                    if(row[0]-1 >= 0 and row[1]-1 >= 0):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]-1][row[1]-1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]-1,row[1]-1])
                    if(row[1]-1 >= 0):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]][row[1]-1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0],row[1]-1])
                    if(row[0]+1 <= 7 and row[1]-1 >= 0):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]+1][row[1]-1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]+1,row[1]-1])
                    if(row[0]-1 >= 0):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]-1][row[1]].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]-1,row[1]])
                    if(row[0]+1 <= 7):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]+1][row[1]].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]+1,row[1]])
                    if(row[0]-1 >= 0 and row[1]+1 <= 7):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]-1][row[1]+1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]-1,row[1]+1])
                    if(row[1]+1 <= 7):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]][row[1]+1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0],row[1]+1])
                    if(row[0]+1 <= 7 and row[1]+1 <= 7):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]+1][row[1]+1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]+1,row[1]+1])
                    for square in listToEnable:
                        if((square in enemyKingPath) and square != [x,y]):
                            squareToRemove.append(square)
                        
                if(row[2] == 'pawn'):
                    if([row[0]-1,row[1]-1] in listToEnable and [row[0]-1,row[1]-1] != [x,y]):
                        listToEnable.pop(listToEnable.index([row[0]-1,row[1]-1]))
                    if([row[0]-1,row[1]+1] in listToEnable and [row[0]-1,row[1]+1] != [x,y]):
                        listToEnable.pop(listToEnable.index([row[0]-1,row[1]+1]))

            for square in squareToRemove:
                    for i in range(8):
                        if(square in listToEnable):
                            listToEnable.pop(listToEnable.index(square))
                        else:
                            break
        elif(color == 'black'):
            enemyPieces = self.pieceFinder('white')
            squareToRemove = []
            for row in enemyPieces:
                if(row[2] == 'rook'):
                    attackPath = self.plan_rook_move(row[0], row[1], 'white', kingCall=True)
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                            checkx, checky, checkColor, checkPiece = self.chessMap[int(square[0])][int(square[1])].cget('text').split('_')
                            if(checkPiece == 'rook'):
                                    squareToRemove.pop(squareToRemove.index(square))
                            if(row[1] == y and row[0] > x and ([x-1,y] in listToEnable) and square == [x+1,y] and (checkPiece == 'rook' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x-1,y])
                            if(row[1] == y and row[0] < x and ([x+1,y] in listToEnable) and square == [x-1,y] and (checkPiece == 'rook' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x+1,y])
                            if(row[0] == x and row[1] > y and ([x, y-1] in listToEnable) and square == [x,y+1] and (checkPiece == 'rook' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x, y-1])
                            if(row[0] == x and row[1] < y and ([x, y+1] in listToEnable) and square == [x,y-1] and (checkPiece == 'rook' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x, y+1])
                if(row[2] == 'knight'):
                    attackPath = self.plan_knight_move(row[0], row[1], 'white', kingCall=True)
                    attackPath.pop(0)
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                if(row[2] == 'bishop'):
                    attackPath = self.plan_bishop_move(row[0], row[1], 'white', kingCall=True)
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                            checkx, checky, checkColor, checkPiece = self.chessMap[int(square[0])][int(square[1])].cget('text').split('_')
                            if(checkPiece == 'bishop'):
                                    squareToRemove.pop(squareToRemove.index(square))
                            if(x-row[0] < 0 and y-row[1] < 0 and (x-row[0] == y-row[1]) and ([x-1,y-1] in listToEnable) and square == [x+1,y+1] and (checkPiece == 'bishop' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x-1,y-1])
                            if(x-row[0] > 0 and y-row[1] > 0 and (x-row[0] == y-row[1]) and ([x+1,y+1] in listToEnable) and square == [x-1,y-1] and (checkPiece == 'bishop' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x+1,y+1])
                            if(row[0]-x > 0 and y-row[1] > 0 and (row[0]-x == y-row[1]) and ([x-1,y+1] in listToEnable) and square == [x+1,y-1] and (checkPiece == 'bishop' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x-1,y+1])
                            if(row[0]-x < 0 and y-row[1] < 0 and (row[0]-x == y-row[1]) and ([x+1,y-1] in listToEnable) and square == [x-1,y+1] and (checkPiece == 'bishop' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x+1,y-1])
                if(row[2] == 'queen'):
                    attackPath = self.plan_queen_move(row[0], row[1], 'white', kingCall=True)
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]): 
                            squareToRemove.append(square)
                            #if the queen is diagnol to the king then the entire diagnol is in threat and the king cannot go backwards on the diagnoal
                            checkx, checky, checkColor, checkPiece = self.chessMap[int(square[0])][int(square[1])].cget('text').split('_')
                            if(checkPiece == 'queen'):
                                    squareToRemove.pop(squareToRemove.index(square))
                            if(x-row[0] < 0 and y-row[1] < 0 and (x-row[0] == y-row[1]) and ([x-1,y-1] in listToEnable) and square == [x+1,y+1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x-1,y-1])
                            if(x-row[0] > 0 and y-row[1] > 0 and (x-row[0] == y-row[1]) and ([x+1,y+1] in listToEnable) and square == [x-1,y-1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x+1,y+1])
                            if(row[0]-x > 0 and y-row[1] > 0 and (row[0]-x == y-row[1]) and ([x-1,y+1] in listToEnable) and square == [x+1,y-1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x-1,y+1])
                            if(row[0]-x < 0 and y-row[1] < 0 and (row[0]-x == y-row[1]) and ([x+1,y-1] in listToEnable) and square == [x-1,y+1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):#if the bishop is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                                squareToRemove.append([x+1,y-1])
                            if(row[1] == y and row[0] > x and ([x-1,y] in listToEnable) and square == [x+1,y] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x-1,y])
                            if(row[1] == y and row[0] < x and ([x+1,y] in listToEnable) and square == [x-1,y] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x+1,y])
                            if(row[0] == x and row[1] > y and ([x, y-1] in listToEnable) and square == [x,y+1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x, y-1])
                            if(row[0] == x and row[1] < y and ([x, y+1] in listToEnable) and square == [x,y-1] and (checkPiece == 'queen' or checkPiece == 'na') and checkColor != color):
                                squareToRemove.append([x, y+1])
                if(row[2] == 'king'):
                    enemyKingPath = [row[0],row[1]]
                    if(row[0]-1 >= 0 and row[1]-1 >= 0):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]-1][row[1]-1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]-1,row[1]-1])
                    if(y-1 >= 0):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]][row[1]-1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0],row[1]-1])
                    if(row[0]+1 <= 7 and row[1]-1 >= 0):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]+1][row[1]-1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]+1,row[1]-1])
                    if(row[0]-1 >= 0):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]-1][row[1]].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]-1,row[1]])
                    if(row[0]+1 <= 7):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]+1][row[1]].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]+1,row[1]])
                    if(row[0]-1 >= 0 and row[1]+1 <= 7):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]-1][row[1]+1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]-1,row[1]+1])
                    if(row[1]+1 <= 7):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]][row[1]+1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0],row[1]+1])
                    if(row[0]+1 <= 7 and row[1]+1 <= 7):
                        newx, newy, newColor, newPiece = self.chessMap[row[0]+1][row[1]+1].cget('text').split('_')
                        if(color != newColor):
                            enemyKingPath.append([row[0]+1,row[1]+1])
                    for square in listToEnable:
                        if((square in enemyKingPath) and square != [x,y]):
                            squareToRemove.append(square)
                if(row[2] == 'pawn'):
                    if([row[0]+1,row[1]-1] in listToEnable and [row[0]+1,row[1]-1] != [x,y]):
                        listToEnable.pop(listToEnable.index([row[0]+1,row[1]-1]))
                    if([row[0]+1,row[1]+1] in listToEnable and [row[0]+1,row[1]+1] != [x,y]):
                        listToEnable.pop(listToEnable.index([row[0]+1,row[1]+1]))
                
            for square in squareToRemove:
                    for i in range(8):
                        if(square in listToEnable):
                            listToEnable.pop(listToEnable.index(square))
                        else:
                            break
        return listToEnable
    
    #function disbales the squares on the board that a player cannot click and enables the buttons that the user can click
    def playerTurn(self, player):
        if(player == 1):
            for row in self.chessMap:
                for col in row:
                    x, y, color, piece = col.cget('text').split('_')
                    if(color == 'white'):
                        col.state(['!disabled'])
                    elif(color == 'black' or color == 'na'):
                        col.state(['disabled'])
            self.P1Turn.config(image = self.Glight)
            self.P2Turn.config(image = self.Rlight)
            self.GPHeaderTitle.config(text = "{}'s Turn".format(ChessGame.P1UserName))

        elif(player == 2):
            for row in self.chessMap:
                for col in row:
                    x, y, color, piece = col.cget('text').split('_')
                    if(color == 'black'):
                        col.state(['!disabled'])
                    elif(color == 'white' or color == 'na'):
                        col.state(['disabled'])
            self.P1Turn.config(image = self.Rlight)
            self.P2Turn.config(image = self.Glight)
            self.GPHeaderTitle.config(text = "{}'s Turn".format(ChessGame.P2UserName))

    def disableButtons(self, listToEnable):
        for row in self.chessMap:
            for col in row:
                col.state(['disabled'])
        for row in listToEnable:
            self.chessMap[row[0]][row[1]].state(['!disabled'])

    def executeMove(self, location):
        currentx, currenty, currentColor, currentPiece = ChessGame.pieceToMove.cget('text').split('_')
        newx, newy, newColor, newPiece = location.cget('text').split('_')

        if(currentColor == 'white' and currentPiece == 'king'):
            ChessGame.P1KING = location
            self.log.config(state = 'normal')
            self.log.insert(END, "{} moved king to {}_{}\n".format(ChessGame.P1UserName, newx,newy))
            self.log.config(state = 'disabled')
        elif(currentColor == 'black' and currentPiece == 'king'):
            ChessGame.P2KING = location
            self.log.config(state = 'normal')
            self.log.insert(END, "{} moved king to {}_{}\n".format(ChessGame.P2UserName, newx,newy))
            self.log.config(state = 'disabled')
        else:
            pass
            

        location.config(text = "{}_{}_{}_{}".format(newx,newy,currentColor,currentPiece))
        ChessGame.pieceToMove.config(text = "{}_{}_{}_{}".format(currentx,currenty,'na','na'))

        if(currentColor == 'white'):
            self.log.config(state = 'normal')
            self.log.insert(END, "{} has moved {} to {}_{} from {}_{}".format(ChessGame.P1UserName,currentPiece, newx, newy, currentx, currenty))
            if(self.checkIfCheck('black')):
                self.log.insert(END, " and put {} in check\n".format(ChessGame.P2UserName))
                self.log.see(END)
                self.log.config(state = 'disabled')
            elif(newColor == 'black'):
                self.log.insert(END, " and taken {}'s {}\n".format(ChessGame.P2UserName, newPiece))
                self.log.see(END)
                self.log.config(state = 'disabled')
            else:
                self.log.insert(END, "\n")
                self.log.see(END)
                self.log.config(state = 'disabled')
        elif(currentColor == 'black'):
            self.log.config(state = 'normal')
            self.log.insert(END, "{} has moved {} to {}_{} from {}_{}".format(ChessGame.P2UserName,currentPiece, newx, newy, currentx, currenty))
            if(self.checkIfCheck('white')):
                self.log.insert(END, " and put {} in check\n".format(ChessGame.P1UserName))
                self.log.see(END)
                self.log.config(state = 'disabled')
            elif(newColor == 'white'):
                self.log.insert(END, " and taken {}'s {}\n".format(ChessGame.P1UserName, newPiece))
                self.log.see(END)
                self.log.config(state = 'disabled')
            else:
                self.log.insert(END, "\n")
                self.log.see(END)
                self.log.config(state = 'disabled')

        if(newColor != 'na'):
            if(currentColor == 'white'):
                self.historyUpdate('white', newPiece, False)
            elif(currentColor == 'black'):
                self.historyUpdate('black', newPiece, False)
            
        if(currentColor == 'white' and currentPiece == 'pawn' and newx == '7'):
            self.openPopUp(currentColor, location)
        elif(currentColor == 'black' and currentPiece == 'pawn' and newx == '0'):
            self.openPopUp(currentColor, location)

        self.fixBoard()

    def pieceFinder(self, colorWanted):
        pieces = []
        for row in self.chessMap:
            for col in row:
                x, y, color, piece = col.cget('text').split('_')
                x = int(x)
                y = int(y)
                if(colorWanted == color):
                    pieces.append([x, y, piece])
                else:
                    pass

        return pieces
    
    def checkIfCheck(self, colorToCheck):
        if(colorToCheck == 'white'):
            kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
            kx = int(kx)
            ky = int(ky)
            piecesThreatning = self.inCheck('white')
            for pieces in piecesThreatning:
                if([kx,ky] in pieces[3]):
                    return True
        elif(colorToCheck == 'black'):
            kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
            kx = int(kx)
            ky = int(ky)
            piecesThreatning = self.inCheck('black')
            for pieces in piecesThreatning:
                if([kx,ky] in pieces[3]):
                    return True
        else:
            return False
    
    def inCheck(self, colorToCheck):#returns a list of enemy pieces threatning the king and the path showing the threat
        piecesThreatning = []
        if(colorToCheck == 'white'):
            enemyPieces = self.pieceFinder('black')
            for piece in enemyPieces:
                if (piece[2] == 'rook'): #When dealing with a rook
                    attackLocations = self.plan_rook_move(piece[0], piece[1], 'black')
                    attackLocations = self.limitingMovement('black', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations): #and rook threatnes king
                        if(kx == piece[0] and ky > piece[1]):# and it is above the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(kx != square[0]):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                                elif(kx == square[0] and square[1] < piece[1]):#remove any squares leading above the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'rook', attackLocations])#add the piece to piecesThreatning list
                        elif(kx == piece[0] and ky < piece[1]):# and it is below the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(kx != square[0]):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                                elif(kx == square[0] and square[1] > piece[1]):#remove any squares down from the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'rook', attackLocations])#add the piece to piecesThreatning list
                        elif(ky == piece[1] and kx > piece[0]):# and it is left of the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(ky != square[1]):#remove any squares leading to up or down from the rook 
                                    squaresToRemove.append(square)
                                elif(ky == square[1] and square[0] < piece[0]):#remove any squares down from the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'rook', attackLocations])#add the piece to piecesThreatning list
                        elif(ky == piece[1] and kx < piece[0]):# and it is right of the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(ky != square[1]):#remove any squares leading to up or down from the rook 
                                    squaresToRemove.append(square)
                                elif(ky == square[1] and square[0] > piece[0]):#remove any squares down from the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'rook', attackLocations])#add the piece to piecesThreatning list
                if(piece[2] == 'bishop'):
                    attackLocations = self.plan_bishop_move(piece[0], piece[1], 'black')
                    attackLocations = self.limitingMovement('black', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations): #and bishop threatnes king
                        if(kx-piece[0] < 0 and ky-piece[1] < 0 and (kx-piece[0] == ky-piece[1])):#if the bishop is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] < piece[0] and square[1] < piece[1])):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'bishop', attackLocations])#add the piece to piecesThreatning list
                        elif(kx-piece[0] > 0 and ky-piece[1] > 0 and (kx-piece[0] == ky-piece[1])):#if the bishop is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] > piece[0] and square[1] > piece[1])):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'bishop', attackLocations])#add the piece to piecesThreatning list
                        elif(piece[0]-kx > 0 and ky-piece[1] > 0 and (piece[0]-kx == ky-piece[1])):#if the bishop is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] < piece[0] and square[1] > piece[1])):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'bishop', attackLocations])#add the piece to piecesThreatning list
                        elif(piece[0]-kx < 0 and ky-piece[1] < 0 and (piece[0]-kx == ky-piece[1])):#if the bishop is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] > piece[0] and square[1] < piece[1])):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'bishop', attackLocations])#add the piece to piecesThreatning list
                        
                if(piece[2] == 'queen'):
                    attackLocations = self.plan_queen_move(piece[0], piece[1], 'black')
                    attackLocations = self.limitingMovement('black', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations): #and queen threatnes king
                        if(kx-piece[0] < 0 and ky-piece[1] < 0 and (kx-piece[0] == ky-piece[1])):#if the queen is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] < piece[0] and square[1] < piece[1])):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(square[0] == piece[0] or square[1] == piece[1]):
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(kx-piece[0] > 0 and ky-piece[1] > 0 and (kx-piece[0] == ky-piece[1])):#if the queen is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] > piece[0] and square[1] > piece[1])):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(square[0] == piece[0] or square[1] == piece[1]):
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(piece[0]-kx > 0 and ky-piece[1] > 0 and (piece[0]-kx == ky-piece[1])):#if the queen is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] < piece[0] and square[1] > piece[1])):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(square[0] == piece[0] or square[1] == piece[1]):
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(piece[0]-kx < 0 and ky-piece[1] < 0 and (piece[0]-kx == ky-piece[1])):#if the queen is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] > piece[0] and square[1] < piece[1])):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(square[0] == piece[0] or square[1] == piece[1]):
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(kx == piece[0] and ky > piece[1]):# and it is above the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(kx != square[0]):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(kx == square[0] and square[1] < piece[1]):#remove any squares leading above the queen 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(kx == piece[0] and ky < piece[1]):# and it is below the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(kx != square[0]):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(kx == square[0] and square[1] > piece[1]):#remove any squares down from the queen 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(ky == piece[1] and kx > piece[0]):# and it is left of the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(ky != square[1]):#remove any squares leading to up or down from the queen 
                                    squaresToRemove.append(square)
                                elif(ky == square[1] and square[0] < piece[0]):#remove any squares down from the queen 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(ky == piece[1] and kx < piece[0]):# and it is right of the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(ky != square[1]):#remove any squares leading to up or down from the queen 
                                    squaresToRemove.append(square)
                                elif(ky == square[1] and square[0] > piece[0]):#remove any squares down from the queen 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                if(piece[2] == 'knight'):
                    attackLocations = self.plan_knight_move(piece[0], piece[1], 'black')
                    attackLocations = self.limitingMovement('black', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations):
                        piecesThreatning.append([piece[0], piece[1], 'knight', [[int(piece[0]), int(piece[1])],[kx,ky]]])
                if(piece[2] == 'pawn'):
                    attackLocations = self.plan_pawn_move(piece[0], piece[1], 'black')
                    attackLocations = self.limitingMovement('black', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations):
                        piecesThreatning.append([piece[0], piece[1], 'pawn', [[int(piece[0]), int(piece[1])],[kx,ky]]])
                if(piece[2] == 'king'):
                    pass
        elif(colorToCheck == 'black'):
            enemyPieces = self.pieceFinder('white')
            for piece in enemyPieces:
                if (piece[2] == 'rook'): #When dealing with a rook
                    attackLocations = self.plan_rook_move(piece[0], piece[1], 'white')
                    attackLocations = self.limitingMovement('white', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations): #and rook threatnes king
                        if(kx == piece[0] and ky > piece[1]):# and it is above the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(kx != square[0]):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                                elif(kx == square[0] and square[1] < piece[1]):#remove any squares leading above the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'rook', attackLocations])#add the piece to piecesThreatning list
                        elif(kx == piece[0] and ky < piece[1]):# and it is below the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(kx != square[0]):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                                elif(kx == square[0] and square[1] > piece[1]):#remove any squares down from the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'rook', attackLocations])#add the piece to piecesThreatning list
                        elif(ky == piece[1] and kx > piece[0]):# and it is left of the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(ky != square[1]):#remove any squares leading to up or down from the rook 
                                    squaresToRemove.append(square)
                                elif(ky == square[1] and square[0] < piece[0]):#remove any squares down from the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'rook', attackLocations])#add the piece to piecesThreatning list
                        elif(ky == piece[1] and kx < piece[0]):# and it is right of the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(ky != square[1]):#remove any squares leading to up or down from the rook 
                                    squaresToRemove.append(square)
                                elif(ky == square[1] and square[0] > piece[0]):#remove any squares down from the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                      
                            piecesThreatning.append([piece[0], piece[1], 'rook', attackLocations])#add the piece to piecesThreatning list
                if(piece[2] == 'bishop'):
                    attackLocations = self.plan_bishop_move(piece[0], piece[1], 'white')
                    attackLocations = self.limitingMovement('white', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations): #and bishop threatnes king
                        if(kx-piece[0] < 0 and ky-piece[1] < 0 and (kx-piece[0] == ky-piece[1])):#if the bishop is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] < piece[0] and square[1] < piece[1])):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                           
                            piecesThreatning.append([piece[0], piece[1], 'bishop', attackLocations])#add the piece to piecesThreatning list
                        elif(kx-piece[0] > 0 and ky-piece[1] > 0 and (kx-piece[0] == ky-piece[1])):#if the bishop is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] > piece[0] and square[1] > piece[1])):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                           
                            piecesThreatning.append([piece[0], piece[1], 'bishop', attackLocations])#add the piece to piecesThreatning list
                        elif(piece[0]-kx > 0 and ky-piece[1] > 0 and (piece[0]-kx == ky-piece[1])):#if the bishop is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] < piece[0] and square[1] > piece[1])):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                           
                            piecesThreatning.append([piece[0], piece[1], 'bishop', attackLocations])#add the piece to piecesThreatning list
                        elif(piece[0]-kx < 0 and ky-piece[1] < 0 and (piece[0]-kx == ky-piece[1])):#if the bishop is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] > piece[0] and square[1] < piece[1])):#remove any squares leading to the left or right of the rook 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            
                            piecesThreatning.append([piece[0], piece[1], 'bishop', attackLocations])#add the piece to piecesThreatning list                        
                if(piece[2] == 'queen'):
                    attackLocations = self.plan_queen_move(piece[0], piece[1], 'white')
                    attackLocations = self.limitingMovement('white', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations): #and rook threatnes king
                        if(kx-piece[0] < 0 and ky-piece[1] < 0 and (kx-piece[0] == ky-piece[1])):#if the queen is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] < piece[0] and square[1] < piece[1])):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(square[0] == piece[0] or square[1] == piece[1]):
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                           
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(kx-piece[0] > 0 and ky-piece[1] > 0 and (kx-piece[0] == ky-piece[1])):#if the queen is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] > piece[0] and square[1] > piece[1])):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(square[0] == piece[0] or square[1] == piece[1]):
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                          
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(piece[0]-kx > 0 and ky-piece[1] > 0 and (piece[0]-kx == ky-piece[1])):#if the queen is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] < piece[0] and square[1] > piece[1])):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(square[0] == piece[0] or square[1] == piece[1]):
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                            
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(piece[0]-kx < 0 and ky-piece[1] < 0 and (piece[0]-kx == ky-piece[1])):#if the queen is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(not(square[0] > piece[0] and square[1] < piece[1])):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(square[0] == piece[0] or square[1] == piece[1]):
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                          
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(kx == piece[0] and ky > piece[1]):# and it is above the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(kx != square[0]):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(kx == square[0] and square[1] < piece[1]):#remove any squares leading above the queen 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                           
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(kx == piece[0] and ky < piece[1]):# and it is below the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(kx != square[0]):#remove any squares leading to the left or right of the queen 
                                    squaresToRemove.append(square)
                                elif(kx == square[0] and square[1] > piece[1]):#remove any squares down from the queen 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                           
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(ky == piece[1] and kx > piece[0]):# and it is left of the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(ky != square[1]):#remove any squares leading to up or down from the queen 
                                    squaresToRemove.append(square)
                                elif(ky == square[1] and square[0] < piece[0]):#remove any squares down from the queen 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))                           
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                        elif(ky == piece[1] and kx < piece[0]):# and it is right of the king
                            squaresToRemove = []
                            for square in attackLocations: #going to remove any path that does not go to the king
                                if([square[0],square[1]] == [piece[0],piece[1]]):
                                    pass
                                elif(ky != square[1]):#remove any squares leading to up or down from the queen 
                                    squaresToRemove.append(square)
                                elif(ky == square[1] and square[0] > piece[0]):#remove any squares down from the queen 
                                    squaresToRemove.append(square)
                            for squares in squaresToRemove:
                                attackLocations.pop(attackLocations.index(squares))
                            piecesThreatning.append([piece[0], piece[1], 'queen', attackLocations])#add the piece to piecesThreatning list
                if(piece[2] == 'knight'):
                    attackLocations = self.plan_knight_move(piece[0], piece[1], 'white')
                    attackLocations = self.limitingMovement('white', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations):
                        piecesThreatning.append([piece[0], piece[1], 'knight', [[int(piece[0]), int(piece[1])],[kx,ky]]])
                if(piece[2] == 'pawn'):
                    attackLocations = self.plan_pawn_move(piece[0], piece[1], 'white')
                    attackLocations = self.limitingMovement('white', attackLocations, piece[2], piece[0], piece[1])
                    kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations):
                        piecesThreatning.append([piece[0], piece[1], 'pawn', [[int(piece[0]), int(piece[1])],[kx,ky]]])
                if(piece[2] == 'king'):
                    pass
        
        return piecesThreatning
    
    def moveablePieces(self, color, piecesThreatning):#returns a list of pieces that can attack currently
        moveable = []
        allPieces = None
        if(color == 'white'):
            allPieces = self.pieceFinder('white')
        elif(color == 'black'):
            allPieces = self.pieceFinder('black')

        if (color == 'white' and len(piecesThreatning) >= 2):
            kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
            kx = int(kx)
            ky = int(ky)
            return([[kx, ky]])
        elif (color == 'black' and len(piecesThreatning) >= 2):
            kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
            kx = int(kx)
            ky = int(ky)
            return([[kx, ky]])

        for piece in allPieces:
            possibleSquare = None
            if (piece[2] == 'rook'):
                possibleSquare = self.plan_rook_move(piece[0], piece[1], color)
                possibleSquare = self.limitingMovement(color, possibleSquare, piece[2], piece[0], piece[1])
            elif(piece[2] == 'bishop'):
                possibleSquare = self.plan_bishop_move(piece[0], piece[1], color)
                possibleSquare = self.limitingMovement(color, possibleSquare, piece[2], piece[0], piece[1])
            elif(piece[2] == 'knight'):
                possibleSquare = self.plan_knight_move(piece[0], piece[1], color)
                possibleSquare = self.limitingMovement(color, possibleSquare, piece[2], piece[0], piece[1])
            elif(piece[2] == 'queen'):
                possibleSquare = self.plan_queen_move(piece[0], piece[1], color)
                possibleSquare = self.limitingMovement(color, possibleSquare, piece[2], piece[0], piece[1])
            elif(piece[2] == 'pawn'):
                possibleSquare = self.plan_pawn_move(piece[0], piece[1], color)
                possibleSquare = self.limitingMovement(color, possibleSquare, piece[2], piece[0], piece[1])
            elif(piece[2] == 'king'):
                possibleSquare = self.plan_king_move(piece[0], piece[1], color)
            
            for square in possibleSquare:
                for location in piecesThreatning:
                    if ([square[0], square[1]] in location[3]):
                        moveable.append([piece[0],piece[1]])

        return moveable

                    
    def checkPlayerTurn(self, player):#resets the board to pieces that are moveable
        if(player == 1):
            piecesThreatning = self.inCheck('white')
            listToEnable = self.moveablePieces('white', piecesThreatning)
            kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
            kx = int(kx)
            ky = int(ky)
            if(listToEnable == [[kx,ky]] and self.plan_king_move(kx, ky, 'white') == [[kx,ky]]):
                self.endGame('black')
            self.disableButtons(listToEnable)
            self.P1Turn.config(image = self.Glight)
            self.P2Turn.config(image = self.Rlight)
            self.GPHeaderTitle.config(text = 'Player 1 Turn')

        elif(player == 2):
            piecesThreatning = self.inCheck('black')
            listToEnable = self.moveablePieces('black', piecesThreatning)
            kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
            kx = int(kx)
            ky = int(ky)
            if(listToEnable == [[kx,ky]] and self.plan_king_move(kx, ky, 'black') == [[kx,ky]]):
                self.endGame('white')
            self.disableButtons(listToEnable)
            self.P1Turn.config(image = self.Rlight)
            self.P2Turn.config(image = self.Glight)
            self.GPHeaderTitle.config(text = 'Player 2 Turn')



    def modified_plan_move(self, x, y, color, piece):
        attackSquares = []
        if(color == 'white'):
            piecesThreatning = self.inCheck('white')
            if(piece == 'pawn'):
                listToEnable = self.plan_pawn_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'rook'):
                listToEnable = self.plan_rook_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'knight'):
                listToEnable = self.plan_knight_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'bishop'):
                listToEnable = self.plan_bishop_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'queen'):
                listToEnable = self.plan_queen_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'king'):
                listToEnable = self.plan_king_move(x, y, color)
                return listToEnable
            
        elif(color == 'black'):
            piecesThreatning = self.inCheck('black')
            if(piece == 'pawn'):
                listToEnable = self.plan_pawn_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'rook'):
                listToEnable = self.plan_rook_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'knight'):
                listToEnable = self.plan_knight_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'bishop'):
                listToEnable = self.plan_bishop_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'queen'):
                listToEnable = self.plan_queen_move(x, y, color)
                attackSquares.append([x,y])
                for square in listToEnable:
                    for location in piecesThreatning:
                        if ([square[0], square[1]] in location[3]):
                            attackSquares.append([square[0],square[1]])
                return attackSquares
            elif(piece == 'king'):
                listToEnable = self.plan_king_move(x, y, color)
                return listToEnable
            
        
    def endGame(self, player):
        if(player == 'white'):
            messagebox.showinfo(title = "Winner", message = "Congratulations {} has won by checkmate".format(ChessGame.P1UserName))
        elif(player == 'black'):
            messagebox.showinfo(title = "Winner", message = "Congratulations {} has won by checkmate".format(ChessGame.P2UserName))
        elif(player == 'stalemate'):
            messagebox.showinfo(title = "Tie", message = "Due to stalemate this is a tie")

        self.disableBoard()

    def checkStalemate(self, color):

        if (color == 'white'):
            allPiece = self.pieceFinder('white')
            amountOfWhitePieces = len(allPiece)
            if(amountOfWhitePieces == 1 and allPiece[0][2] == 'king'):
                blackPiece = self.pieceFinder('black')
                amountOfBlackPieces = len(blackPiece)
                if(amountOfBlackPieces == 1 and blackPiece[0][2] == 'king'):
                    return True
        elif(color == 'black'):
            allPiece = self.pieceFinder('black')
            amountOfBlackPieces = len(allPiece)
            if(amountOfBlackPieces == 1 and allPiece[0][2] == 'king'):
                blackPiece = self.pieceFinder('white')
                amountOfWhitePieces = len(blackPiece)
                if(amountOfWhitePieces == 1 and blackPiece[0][2] == 'king'):
                    return True

        for piece in allPiece:
            if (piece[2] == 'pawn'):
                attackLocation = self.plan_pawn_move(piece[0], piece[1], color)
            elif(piece[2] == 'rook'):
                attackLocation = self.plan_rook_move(piece[0], piece[1], color)
            elif(piece[2] == 'knight'):
                attackLocation = self.plan_knight_move(piece[0], piece[1], color)
            elif(piece[2] == 'bishop'):
                attackLocation = self.plan_bishop_move(piece[0], piece[1], color)
            elif(piece[2] == 'queen'):
                attackLocation = self.plan_queen_move(piece[0], piece[1], color)
            elif(piece[2] == 'king'):
                attackLocation = self.plan_king_move(piece[0], piece[1], color)

            if(attackLocation != [[piece[0], piece[1]]]):
                return False
        
        return True

    def addImages(self):
        if(ChessGame.P1Color == 'white'):
            self.W_Pawn = PhotoImage(file = 'ChessGame/Pieces/W_Pawn.gif')
            self.W_Rook = PhotoImage(file = 'ChessGame/Pieces/W_Rook.gif')
            self.W_Knight = PhotoImage(file = 'ChessGame/Pieces/W_Knight.gif')
            self.W_Bishop = PhotoImage(file = 'ChessGame/Pieces/W_Bishop.gif')
            self.W_Queen = PhotoImage(file = 'ChessGame/Pieces/W_Queen.gif')
            self.W_King = PhotoImage(file = 'ChessGame/Pieces/W_King.gif')
        elif(ChessGame.P1Color == 'black'):
            self.W_Pawn = PhotoImage(file = 'ChessGame/Pieces/B_Pawn.gif')
            self.W_Rook = PhotoImage(file = 'ChessGame/Pieces/B_Rook.gif')
            self.W_Knight = PhotoImage(file = 'ChessGame/Pieces/B_Knight.gif')
            self.W_Bishop = PhotoImage(file = 'ChessGame/Pieces/B_Bishop.gif')
            self.W_Queen = PhotoImage(file = 'ChessGame/Pieces/B_Queen.gif')
            self.W_King = PhotoImage(file = 'ChessGame/Pieces/B_King.gif')
        elif(ChessGame.P1Color == 'green'):
            self.W_Pawn = PhotoImage(file = 'ChessGame/Pieces/G_Pawn.gif')
            self.W_Rook = PhotoImage(file = 'ChessGame/Pieces/G_Rook.gif')
            self.W_Knight = PhotoImage(file = 'ChessGame/Pieces/G_Knight.gif')
            self.W_Bishop = PhotoImage(file = 'ChessGame/Pieces/G_Bishop.gif')
            self.W_Queen = PhotoImage(file = 'ChessGame/Pieces/G_Queen.gif')
            self.W_King = PhotoImage(file = 'ChessGame/Pieces/G_King.gif')
        elif(ChessGame.P1Color == 'red'):
            self.W_Pawn = PhotoImage(file = 'ChessGame/Pieces/R_Pawn.gif')
            self.W_Rook = PhotoImage(file = 'ChessGame/Pieces/R_Rook.gif')
            self.W_Knight = PhotoImage(file = 'ChessGame/Pieces/R_Knight.gif')
            self.W_Bishop = PhotoImage(file = 'ChessGame/Pieces/R_Bishop.gif')
            self.W_Queen = PhotoImage(file = 'ChessGame/Pieces/R_Queen.gif')
            self.W_King = PhotoImage(file = 'ChessGame/Pieces/R_King.gif')
        elif(ChessGame.P1Color == 'gold'):
            self.W_Pawn = PhotoImage(file = 'ChessGame/Pieces/Go_Pawn.gif')
            self.W_Rook = PhotoImage(file = 'ChessGame/Pieces/Go_Rook.gif')
            self.W_Knight = PhotoImage(file = 'ChessGame/Pieces/Go_Knight.gif')
            self.W_Bishop = PhotoImage(file = 'ChessGame/Pieces/Go_Bishop.gif')
            self.W_Queen = PhotoImage(file = 'ChessGame/Pieces/Go_Queen.gif')
            self.W_King = PhotoImage(file = 'ChessGame/Pieces/Go_King.gif')
        
        if(ChessGame.P2Color == 'white'):
            self.B_Pawn = PhotoImage(file = 'ChessGame/Pieces/W_Pawn.gif')
            self.B_Rook = PhotoImage(file = 'ChessGame/Pieces/W_Rook.gif')
            self.B_Knight = PhotoImage(file = 'ChessGame/Pieces/W_Knight.gif')
            self.B_Bishop = PhotoImage(file = 'ChessGame/Pieces/W_Bishop.gif')
            self.B_Queen = PhotoImage(file = 'ChessGame/Pieces/W_Queen.gif')
            self.B_King = PhotoImage(file = 'ChessGame/Pieces/W_King.gif')
        elif(ChessGame.P2Color == 'black'):
            self.B_Pawn = PhotoImage(file = 'ChessGame/Pieces/B_Pawn.gif')
            self.B_Rook = PhotoImage(file = 'ChessGame/Pieces/B_Rook.gif')
            self.B_Knight = PhotoImage(file = 'ChessGame/Pieces/B_Knight.gif')
            self.B_Bishop = PhotoImage(file = 'ChessGame/Pieces/B_Bishop.gif')
            self.B_Queen = PhotoImage(file = 'ChessGame/Pieces/B_Queen.gif')
            self.B_King = PhotoImage(file = 'ChessGame/Pieces/B_King.gif')
        elif(ChessGame.P2Color == 'green'):
            self.B_Pawn = PhotoImage(file = 'ChessGame/Pieces/G_Pawn.gif')
            self.B_Rook = PhotoImage(file = 'ChessGame/Pieces/G_Rook.gif')
            self.B_Knight = PhotoImage(file = 'ChessGame/Pieces/G_Knight.gif')
            self.B_Bishop = PhotoImage(file = 'ChessGame/Pieces/G_Bishop.gif')
            self.B_Queen = PhotoImage(file = 'ChessGame/Pieces/G_Queen.gif')
            self.B_King = PhotoImage(file = 'ChessGame/Pieces/G_King.gif')
        elif(ChessGame.P2Color == 'red'):
            self.B_Pawn = PhotoImage(file = 'ChessGame/Pieces/R_Pawn.gif')
            self.B_Rook = PhotoImage(file = 'ChessGame/Pieces/R_Rook.gif')
            self.B_Knight = PhotoImage(file = 'ChessGame/Pieces/R_Knight.gif')
            self.B_Bishop = PhotoImage(file = 'ChessGame/Pieces/R_Bishop.gif')
            self.B_Queen = PhotoImage(file = 'ChessGame/Pieces/R_Queen.gif')
            self.B_King = PhotoImage(file = 'ChessGame/Pieces/R_King.gif')
        elif(ChessGame.P2Color == 'gold'):
            self.B_Pawn = PhotoImage(file = 'ChessGame/Pieces/Go_Pawn.gif')
            self.B_Rook = PhotoImage(file = 'ChessGame/Pieces/Go_Rook.gif')
            self.B_Knight = PhotoImage(file = 'ChessGame/Pieces/Go_Knight.gif')
            self.B_Bishop = PhotoImage(file = 'ChessGame/Pieces/Go_Bishop.gif')
            self.B_Queen = PhotoImage(file = 'ChessGame/Pieces/Go_Queen.gif')
            self.B_King = PhotoImage(file = 'ChessGame/Pieces/Go_King.gif')
 
        self.background = PhotoImage(file = 'ChessGame/Pieces/background.gif')

    def fixBoard(self):
        for row in self.chessMap:
            for square in row:
                x, y, color, piece = square.cget('text').split('_')
                if(color == 'white'):
                    if(piece == 'pawn'):
                        square.config(image = self.W_Pawn)
                    elif(piece == 'rook'):
                        square.config(image = self.W_Rook)
                    elif(piece == 'knight'):
                        square.config(image = self.W_Knight)
                    elif(piece == 'bishop'):
                        square.config(image = self.W_Bishop)
                    elif(piece == 'queen'):
                        square.config(image = self.W_Queen)
                    elif(piece == 'king'):
                        square.config(image = self.W_King)
                elif(color == 'black'):
                    if(piece == 'pawn'):
                        square.config(image = self.B_Pawn)
                    elif(piece == 'rook'):
                        square.config(image = self.B_Rook)
                    elif(piece == 'knight'):
                        square.config(image = self.B_Knight)
                    elif(piece == 'bishop'):
                        square.config(image = self.B_Bishop)
                    elif(piece == 'queen'):
                        square.config(image = self.B_Queen)
                    elif(piece == 'king'):
                        square.config(image = self.B_King)
                elif(color == 'na'):
                    square.config(image = self.background)

    def limitingMovement(self, color, listToChange, freindlyPiece, x, y):
        if(color == 'white'):
            allPieces = self.pieceFinder('black')
        elif(color == 'black'):
            allPieces = self.pieceFinder('white')

        for piece in allPieces:
            if(piece[2] == 'rook'):
                futAttackLocations = self.plan_rook_move(piece[0], piece[1], piece[2], checkCall=True)
                if(futAttackLocations == False):
                    pass
                elif(futAttackLocations[0][2] == freindlyPiece and futAttackLocations[0][0] == x and futAttackLocations[0][1] == y):
                    squareToRemove = []
                    for square in listToChange:
                        if(square in futAttackLocations[1]):
                            pass
                        else:
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToChange.pop(listToChange.index(square))
                    break
            elif(piece[2] == 'bishop'):
                futAttackLocations = self.plan_bishop_move(piece[0], piece[1], piece[2], checkCall=True)
                if(futAttackLocations == False):
                    pass
                elif(futAttackLocations[0][2] == freindlyPiece and futAttackLocations[0][0] == x and futAttackLocations[0][1] == y):
                    squareToRemove = []
                    for square in listToChange:
                        if(square in futAttackLocations[1]):
                            pass
                        else:
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToChange.pop(listToChange.index(square))
                    break
            elif(piece[2] == 'queen'):
                futAttackLocations = self.plan_queen_move(piece[0], piece[1], piece[2], checkCall=True)
                if(futAttackLocations == False):
                    pass
                elif(futAttackLocations[0][2] == freindlyPiece and futAttackLocations[0][0] == x and futAttackLocations[0][1] == y):
                    squareToRemove = []
                    for square in listToChange:
                        if(square in futAttackLocations[1]):
                            pass
                        else:
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToChange.pop(listToChange.index(square))
                    break
        return listToChange
            
    def historyUpdate(self, color, newPiece, up = False):
        if(color == 'white'):
            self.P2Hist.config(state = 'normal')
            if(newPiece == 'rook' and up == True):
                self.P1Hist.config(state = 'normal')
                self.P1Hist.insert('6.6', str(int(self.P1Hist.get('6.6'))+1))
                self.P1Hist.delete('6.7')
                self.P1Hist.config(state = 'disabled')
            elif(newPiece == 'knight' and up == True):
                self.P1Hist.config(state = 'normal')
                self.P1Hist.insert('5.8', str(int(self.P1Hist.get('5.8'))+1))
                self.P1Hist.delete('5.9')
                self.P1Hist.config(state = 'disabled')
            elif(newPiece == 'bishop' and up == True):
                self.P1Hist.config(state = 'normal')
                self.P1Hist.insert('4.8', str(int(self.P1Hist.get('4.8'))+1))
                self.P1Hist.delete('4.9')
                self.P1Hist.config(state = 'disabled')
            elif(newPiece == 'queen' and up == True):
                self.P1Hist.config(state = 'normal')
                self.P1Hist.insert('3.7', str(int(self.P1Hist.get('3.7'))+1))
                self.P1Hist.delete('3.8')
                self.P1Hist.config(state = 'disabled')
            elif(newPiece == 'pawn'):
                self.P2Hist.insert('7.6', str(int(self.P2Hist.get('7.6'))-1))
                self.P2Hist.delete('7.7')
            elif(newPiece == 'rook'):
                self.P2Hist.insert('6.6', str(int(self.P2Hist.get('6.6'))-1))
                self.P2Hist.delete('6.7')
            elif(newPiece == 'knight'):
                self.P2Hist.insert('5.8', str(int(self.P2Hist.get('5.8'))-1))
                self.P2Hist.delete('5.9')
            elif(newPiece == 'bishop'):
                self.P2Hist.insert('4.8', str(int(self.P2Hist.get('4.8'))-1))
                self.P2Hist.delete('4.9')
            elif(newPiece == 'queen'):
                self.P2Hist.insert('3.7', str(int(self.P2Hist.get('3.7'))-1))
                self.P2Hist.delete('3.8')
            self.P2Hist.config(state = 'disabled')
        elif(color == 'black'):
            self.P1Hist.config(state = 'normal')
            if(newPiece == 'rook' and up == True):
                self.P2Hist.config(state = 'normal')
                self.P2Hist.insert('6.6', str(int(self.P2Hist.get('6.6'))+1))
                self.P2Hist.delete('6.7')
                self.P2Hist.config(state = 'disabled')
            elif(newPiece == 'knight' and up == True):
                self.P2Hist.config(state = 'normal')
                self.P2Hist.insert('5.8', str(int(self.P2Hist.get('5.8'))+1))
                self.P2Hist.delete('5.9')
                self.P2Hist.config(state = 'disabled')
            elif(newPiece == 'bishop' and up == True):
                self.P2Hist.config(state = 'normal')
                self.P2Hist.insert('4.8', str(int(self.P2Hist.get('4.8'))+1))
                self.P2Hist.delete('4.9')
                self.P2Hist.config(state = 'disabled')
            elif(newPiece == 'queen' and up == True):
                self.P2Hist.config(state = 'normal')
                self.P2Hist.insert('3.7', str(int(self.P2Hist.get('3.7'))+1))
                self.P2Hist.delete('3.8')
                self.P2Hist.config(state = 'disabled')
            elif(newPiece == 'pawn'):
                self.P1Hist.insert('7.6', str(int(self.P1Hist.get('7.6'))-1))
                self.P1Hist.delete('7.7')
            elif(newPiece == 'rook'):
                self.P1Hist.insert('6.6', str(int(self.P1Hist.get('6.6'))-1))
                self.P1Hist.delete('6.7')
            elif(newPiece == 'knight'):
                self.P1Hist.insert('5.8', str(int(self.P1Hist.get('5.8'))-1))
                self.P1Hist.delete('5.9')
            elif(newPiece == 'bishop'):
                self.P1Hist.insert('4.8', str(int(self.P1Hist.get('4.8'))-1))
                self.P1Hist.delete('4.9')
            elif(newPiece == 'queen'):
                self.P1Hist.insert('3.7', str(int(self.P1Hist.get('3.7'))-1))
                self.P1Hist.delete('3.8')
            self.P1Hist.config(state = 'disabled')

    def openPopUp(self, color, location):
        self.popUp = Toplevel(ChessGame.topLevelFrame)
        self.label = ttk.Label(self.popUp, text = 'Pawn Reached enemy base what piece would you like?', font=('Courier', 12), background = 'light blue')
        self.rookOption = ttk.Button(self.popUp, text = 'rook')
        self.bishopOption = ttk.Button(self.popUp, text = 'bishop')
        self.knightOption = ttk.Button(self.popUp, text = 'knight')
        self.queenOption = ttk.Button(self.popUp, text = 'queen')

        self.label.grid(row = 0, column = 0)
        self.rookOption.grid(row = 1, column = 0)
        self.bishopOption.grid(row = 2, column = 0)
        self.knightOption.grid(row = 3, column = 0)
        self.queenOption.grid(row = 4, column = 0)

        self.popUp.rowconfigure(0, weight=1)
        self.popUp.rowconfigure(1, weight=1)
        self.popUp.rowconfigure(2, weight=1)
        self.popUp.rowconfigure(3, weight=1)
        self.popUp.rowconfigure(4, weight=1)
        self.popUp.columnconfigure(0, weight=1)

        if(color == 'white'):
            self.rookOption.config(image = self.W_Rook, style = 'White.TButton', command = lambda: self.pawnExchange(self.rookOption, self.popUp, location))
            self.bishopOption.config(image = self.W_Bishop, style = 'White.TButton', command = lambda: self.pawnExchange(self.bishopOption, self.popUp, location))
            self.knightOption.config(image = self.W_Knight, style = 'White.TButton', command = lambda: self.pawnExchange(self.knightOption, self.popUp, location))
            self.queenOption.config(image = self.W_Queen, style = 'White.TButton', command = lambda: self.pawnExchange(self.queenOption, self.popUp, location))
        elif(color == 'black'):
            self.rookOption.config(image = self.B_Rook, style = 'Black.TButton', command = lambda: self.pawnExchange(self.rookOption, self.popUp, location))
            self.bishopOption.config(image = self.B_Bishop, style = 'Black.TButton', command = lambda: self.pawnExchange(self.bishopOption, self.popUp, location))
            self.knightOption.config(image = self.B_Knight, style = 'Black.TButton', command = lambda: self.pawnExchange(self.knightOption, self.popUp, location))
            self.queenOption.config(image = self.B_Queen, style = 'Black.TButton', command = lambda: self.pawnExchange(self.queenOption, self.popUp, location))

    def pawnExchange(self, piece, frame, location):
            locx, locy, locColor, locPiece = location.cget('text').split('_')
            newPiece = piece.cget('text')
            location.config(text = "{}_{}_{}_{}".format(locx, locy, locColor, newPiece))
            frame.destroy()
            self.historyUpdate(locColor, newPiece, True)
            self.fixBoard()

    def surrenderCommand(self):
        self.surrPopUp = Toplevel(ChessGame.topLevelFrame)

        self.surrLabel = ttk.Label(self.surrPopUp, text= "Who is surrrendering?", font = ('Courier', 12), background = 'light blue')
        self.Player1Button = ttk.Button(self.surrPopUp, text = '{}'.format(ChessGame.P1UserName), command = lambda: self.surrDisableButton(self.Player1Button), style = 'White.TButton')
        self.Player2Button = ttk.Button(self.surrPopUp, text = '{}'.format(ChessGame.P2UserName), command = lambda: self.surrDisableButton(self.Player2Button), style = 'Black.TButton')
        self.passLabel = ttk.Label(self.surrPopUp, text = "Password")
        self.surrEntry = ttk.Entry(self.surrPopUp)
        self.submitSurrButton = ttk.Button(self.surrPopUp, text = 'Submit Password', command = lambda: self.surrPassCheck(self.surrPopUp, self.surrEntry))

        self.surrLabel.grid(row = 0, column = 0, columnspan=2)
        self.Player1Button.grid(row = 1, column = 0)
        self.Player2Button.grid(row = 1, column = 1)
        self.passLabel.grid(row = 2, column = 0, columnspan = 2)
        self.surrEntry.grid(row = 3, column = 0, columnspan = 2)
        self.submitSurrButton.grid(row = 4, column = 0, columnspan = 2)

    def surrDisableButton(self, button):
        self.surrenderingPlayer = None
        if(button == self.Player1Button):
            if(self.Player2Button.state() == ('disabled',)):
                self.Player2Button.state(['!disabled'])
                self.surrenderingPlayer = ""
            elif(self.Player2Button.state() == ()):
                self.Player2Button.state(['disabled'])
                self.surrenderingPlayer = "Player 1"
        elif(button == self.Player2Button):
            if(self.Player1Button.state() == ('disabled',)):
                self.Player1Button.state(['!disabled'])
                self.surrenderingPlayer = ""
            elif(self.Player1Button.state() == ()):
                self.Player1Button.state(['disabled'])
                self.surrenderingPlayer = "Player 2"

    def surrPassCheck(self, frame, entryWidget):
        if(self.surrenderingPlayer == ""):
            messagebox.showerror(title = "ERROR", message = "Please pick who wants to surrender")
        elif(entryWidget.get() == ""):
            messagebox.showerror(title = "ERROR", message = "Please Provide the password")
        else:
            if(self.surrenderingPlayer == 'Player 1'):
                if(entryWidget.get() == ChessGame.P1Pass):
                    self.endGame('black')
                else:
                    messagebox.showerror(title = "Password Wrong", message = 'The wrong password was put it for player 1')
            elif(self.surrenderingPlayer == 'Player 2'):
                if(entryWidget.get() == ChessGame.P2Pass):
                    self.endGame('white')
                else:
                    messagebox.showerror(title = "Password Wrong", message = 'The wrong password was put it for player 2')

        
    def disableBoard(self):
        for row in self.chessMap:
            for square in row:
                square.state(['disabled'])

    
def main():
    root = Tk()
    chess = ChessGame(root)
    root.mainloop()


if __name__ == "__main__": main()