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
    state = GameState.WELCOMEPAGE
    pieceToMove = None
    P1KING = None
    P2KING = None
    
    

    def __init__(self, master):
        #Intialize Welcome Page with Frames and pack them to root page
        master.title('FuzzChess')
        
        #master.geometry('950x550')

        #Intializing Style Object
        self.style = ttk.Style()
        self.style.theme_use('classic')

        #Creating a notebook
        self.notebook = ttk.Notebook(master)
        self.notebook.pack()

        #Creating Frames two pages
        self.welcomePage = ttk.Frame(self.notebook)
        self.gamePage = ttk.Frame(self.notebook)

        #adding the welcome page
        self.notebook.add(self.welcomePage, text = 'Welcome Page')

        #Frames for Welcome Page
        self.headerFrame = ttk.Frame(self.welcomePage)
        self.userChoiceFrame = ttk.Frame(self.welcomePage)
        
        #pack the frames
        self.headerFrame.pack()
        self.userChoiceFrame.pack()

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
        
        
        ttk.Label(self.headerFrame, image = self.imgWP).pack(side = LEFT)
        ttk.Label(self.headerFrame, text = "Welcome to Fuzail's Chess Game", font= ('Courier', 22), background = 'light blue').pack(side=LEFT)
        ttk.Label(self.headerFrame, image = self.imgBP).pack(side = LEFT)

        #Widgets for the userChoice Frame. Add the two Labels, 7 buttons and 2 entry boxes
        ttk.Label(self.userChoiceFrame, text = 'Player 1 Choose Color').grid(row = 0, column = 0, columnspan = 3)
        ttk.Label(self.userChoiceFrame, text = 'Player 2 Choose Color').grid(row = 0, column = 4, columnspan = 3)

        #Adding White, Black, grey styles
        self.style.configure('WC.TButton', background = 'white', foreground = 'black')
        self.style.configure('BC.TButton', background = 'black', foreground = 'white')
        self.style.configure('GC.TButton', background = 'Gray', foreground = 'red')

        self.style.map('WC.TButton', background = [('active', 'bisque4'), ('disabled','azure3')], foreground = [('active', 'black'), ('disabled','azure2')])
        self.style.map('BC.TButton', background = [('active', 'bisque4'), ('disabled','azure3')], foreground = [('active', 'black'), ('disabled','azure2')])
        self.style.map('GC.TButton', background = [('active', 'bisque4'), ('disabled','azure3')], foreground = [('active', 'black'), ('disabled','azure2')])

        self.P1WhiteB = ttk.Button(self.userChoiceFrame, text = 'White', command = self.p1WhitePress, style = 'WC.TButton')
        self.P1WhiteB.grid(row = 1, column = 0, padx = 5)
        self.P2WhiteB = ttk.Button(self.userChoiceFrame, text = 'White', command = self.p2WhitePress, style = 'WC.TButton')
        self.P2WhiteB.grid(row = 1, column = 4, padx = 5)

        self.P1BlackB = ttk.Button(self.userChoiceFrame, text = 'Black', command = self.p1BlackPress, style = 'BC.TButton')
        self.P1BlackB.grid(row = 1, column = 1, padx = 5)
        self.P2BlackB = ttk.Button(self.userChoiceFrame, text = 'Black', command = self.p2BlackPress, style = 'BC.TButton')
        self.P2BlackB.grid(row = 1, column = 5, padx = 5)

        self.P1GreyB = ttk.Button(self.userChoiceFrame, text = 'Grey', command = self.p1GreyPress, style = 'GC.TButton')
        self.P1GreyB.grid(row = 1, column = 2, padx = 5)
        self.P2GreyB = ttk.Button(self.userChoiceFrame, text = 'Grey', command = self.p2GreyPress, style = 'GC.TButton')
        self.P2GreyB.grid(row = 1, column = 6, padx = 5)

        self.submit = ttk.Button(self.userChoiceFrame, text = "Let's Chess!!!", command = self.submit)
        self.submit.grid(row = 3, column = 3, pady = 10)
        
        self.P1PasswordValue = ttk.Entry(self.userChoiceFrame, text = 'Password Player 1', show = '*')
        self.P1PasswordValue.grid(row = 3, column = 0, columnspan = 3)
        self.P2PasswordValue = ttk.Entry(self.userChoiceFrame, text = 'Password Player 2', show = '*')
        self.P2PasswordValue.grid(row = 3, column = 4, columnspan = 3)

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

        #add three label widgets to the header 
        ttk.Label(self.headerGPFrame, image = self.imgWP).pack(side = LEFT)
        self.GPHeaderTitle = ttk.Label(self.headerGPFrame, font = ('Courier', 22), background = 'light blue')
        self.GPHeaderTitle.pack(side = LEFT)
        ttk.Label(self.headerGPFrame, image = self.imgBP).pack(side = LEFT)

        #add the widgets for the P1GFrame 
        ttk.Label(self.P1Frame, text = 'Player 1').grid(row = 0, column = 0)
        self.P1Hist = Text(self.P1Frame, width = 30, height = 5, wrap = 'word')
        self.P1Hist.grid(row = 1, column = 0, columnspan = 2)
        self.P1Hist.insert('1.0', 'Player 1 History')
        self.P1Hist.config(state = 'disabled')
        self.Glight = PhotoImage(file = 'ChessGame/GreenLight.gif').subsample(40, 40)
        self.P1Turn = ttk.Label(self.P1Frame, image = self.Glight)
        self.P1Turn.grid(row = 0, column = 1)

        #add the widgets for the P2GFrame
        ttk.Label(self.P2Frame, text = 'Player 2').grid(row = 0, column = 0)
        self.P2Hist = Text(self.P2Frame, width = 30, height = 5, wrap = 'word')
        self.P2Hist.grid(row = 1, column = 0, columnspan = 2)
        self.P2Hist.insert('1.0', 'Player 2 History')
        self.P2Hist.config(state = 'disabled')
        self.Rlight = PhotoImage(file = 'ChessGame/RedLight.gif').subsample(27, 27)
        self.P2Turn = ttk.Label(self.P2Frame, image = self.Rlight)
        self.P2Turn.grid(row = 0, column = 1)

        #Add the widgets for the logFrame
        ttk.Label(self.LogFrame, text = 'Game Log').pack()
        self.log = Text(self.LogFrame, width = 30, height = 5)
        self.log.insert('1.0', 'Game Log will be shown here:')
        self.log.config(state = 'disabled')
        self.log.pack()

        #Add the widgets for the buttonFrame
        self.surrenderButton = ttk.Button(self.buttonsFrame, text = 'Surrender', padding = 5)
        self.exitButton = ttk.Button(self.buttonsFrame, text = 'Exit', padding = 5, command = master.destroy)
        self.surrenderButton.grid(row = 0, column = 0)
        self.exitButton.grid(row = 1, column = 0)

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

        self.addImages()
        
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

        self.C0 = ttk.Button(self.CBFrame, text = '2_0_na_na', image = self.background, style = 'Black.TButton', command = lambda: self.buttonCommand(self.C0))
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

        #Create the chess map in the background 
        self.createMap()
        self.fixBoard()

    def p1WhitePress(self):
        if (ChessGame.P1Color == "" and ChessGame.P2Color == ""):
            self.P2WhiteB.state(['disabled'])
            self.P1BlackB.state(['disabled'])
            self.P1GreyB.state(['disabled'])
            ChessGame.P1Color = "white"
        elif(ChessGame.P1Color != "" and ChessGame.P2Color == ""):
            self.P2WhiteB.state(['!disabled'])
            self.P1BlackB.state(['!disabled'])
            self.P1GreyB.state(['!disabled'])
            ChessGame.P1Color = ""
        elif(ChessGame.P1Color == "" and ChessGame.P2Color != ""):
            if(ChessGame.P2Color == "black"):
                self.P1GreyB.state(['disabled'])
            else:
                self.P1BlackB.state(['disabled'])
            ChessGame.P1Color = "white"
        else:
            if(ChessGame.P2Color == 'black'):
                self.P1GreyB.state(['!disabled'])
            else:
                self.P1BlackB.state(['!disabled'])
            ChessGame.P1Color = ""
        print('Player 1 color picked: {}'.format(ChessGame.P1Color))
        print('Player 2 color picked: {}'.format(ChessGame.P2Color))

    def p2WhitePress(self):
        if (ChessGame.P2Color == "" and ChessGame.P1Color == ""):
            self.P1WhiteB.state(['disabled'])
            self.P2BlackB.state(['disabled'])
            self.P2GreyB.state(['disabled'])
            ChessGame.P2Color = "white"
        elif(ChessGame.P2Color != "" and ChessGame.P1Color == ""):
            self.P1WhiteB.state(['!disabled'])
            self.P2BlackB.state(['!disabled'])
            self.P2GreyB.state(['!disabled'])
            ChessGame.P2Color = ""
        elif(ChessGame.P2Color == "" and ChessGame.P1Color != ""):
            if(ChessGame.P1Color == "black"):
                self.P2GreyB.state(['disabled'])
            else:
                self.P2BlackB.state(['disabled'])
            ChessGame.P2Color = "white"
        else:
            if(ChessGame.P1Color == 'black'):
                self.P2GreyB.state(['!disabled'])
            else:
                self.P2BlackB.state(['!disabled'])
            ChessGame.P2Color = ""
        print('Player 1 color picked: {}'.format(ChessGame.P1Color))
        print('Player 2 color picked: {}'.format(ChessGame.P2Color))

    def p1BlackPress(self):
        if (ChessGame.P1Color == "" and ChessGame.P2Color == ""):
            self.P2BlackB.state(['disabled'])
            self.P1WhiteB.state(['disabled'])
            self.P1GreyB.state(['disabled'])
            ChessGame.P1Color = "black"
        elif(ChessGame.P1Color != "" and ChessGame.P2Color == ""):
            self.P2BlackB.state(['!disabled'])
            self.P1WhiteB.state(['!disabled'])
            self.P1GreyB.state(['!disabled'])
            ChessGame.P1Color = ""
        elif(ChessGame.P1Color == "" and ChessGame.P2Color != ""):
            if(ChessGame.P2Color == "white"):
                self.P1GreyB.state(['disabled'])
            else:
                self.P1WhiteB.state(['disabled'])
            ChessGame.P1Color = "black"
        else:
            if(ChessGame.P2Color == 'white'):
                self.P1GreyB.state(['!disabled'])
            else:
                self.P1WhiteB.state(['!disabled'])
            ChessGame.P1Color = ""
        print('Player 1 color picked: {}'.format(ChessGame.P1Color))
        print('Player 2 color picked: {}'.format(ChessGame.P2Color))
    
    def p2BlackPress(self):
        if (ChessGame.P2Color == "" and ChessGame.P1Color == ""):
            self.P1BlackB.state(['disabled'])
            self.P2WhiteB.state(['disabled'])
            self.P2GreyB.state(['disabled'])
            ChessGame.P2Color = "black"
        elif(ChessGame.P2Color != "" and ChessGame.P1Color == ""):
            self.P1BlackB.state(['!disabled'])
            self.P2WhiteB.state(['!disabled'])
            self.P2GreyB.state(['!disabled'])
            ChessGame.P2Color = ""
        elif(ChessGame.P2Color == "" and ChessGame.P1Color != ""):
            if(ChessGame.P1Color == "white"):
                self.P2GreyB.state(['disabled'])
            else:
                self.P2WhiteB.state(['disabled'])
            ChessGame.P2Color = "black"
        else:
            if(ChessGame.P1Color == 'grey'):
                self.P2WhiteB.state(['!disabled'])
            else:
                self.P2GreyB.state(['!disabled'])
            ChessGame.P2Color = ""
        print('Player 1 color picked: {}'.format(ChessGame.P1Color))
        print('Player 2 color picked: {}'.format(ChessGame.P2Color))

    def p1GreyPress(self):
        if (ChessGame.P1Color == "" and ChessGame.P2Color == ""):
            self.P2GreyB.state(['disabled'])
            self.P1WhiteB.state(['disabled'])
            self.P1BlackB.state(['disabled'])
            ChessGame.P1Color = "grey"
        elif(ChessGame.P1Color != "" and ChessGame.P2Color == ""):
            self.P2GreyB.state(['!disabled'])
            self.P1WhiteB.state(['!disabled'])
            self.P1BlackB.state(['!disabled'])
            ChessGame.P1Color = ""
        elif(ChessGame.P1Color == "" and ChessGame.P2Color != ""):
            if(ChessGame.P2Color == "black"):
                self.P1WhiteB.state(['disabled'])
            else:
                self.P1BlackB.state(['disabled'])
            ChessGame.P1Color = "grey"
        else:
            if(ChessGame.P2Color == 'white'):
                self.P1BlackB.state(['!disabled'])
            else:
                self.P1WhiteB.state(['!disabled'])
            ChessGame.P1Color = ""
        print('Player 1 color picked: {}'.format(ChessGame.P1Color))
        print('Player 2 color picked: {}'.format(ChessGame.P2Color))

    def p2GreyPress(self):
        if (ChessGame.P2Color == "" and ChessGame.P1Color == ""):
            self.P1GreyB.state(['disabled'])
            self.P2WhiteB.state(['disabled'])
            self.P2BlackB.state(['disabled'])
            ChessGame.P2Color = "grey"
        elif(ChessGame.P2Color != "" and ChessGame.P1Color == ""):
            self.P1GreyB.state(['!disabled'])
            self.P2WhiteB.state(['!disabled'])
            self.P2BlackB.state(['!disabled'])
            ChessGame.P2Color = ""
        elif(ChessGame.P2Color == "" and ChessGame.P1Color != ""):
            if(ChessGame.P1Color == "black"):
                self.P2WhiteB.state(['disabled'])
            else:
                self.P2BlackB.state(['disabled'])
            ChessGame.P2Color = "grey"
        else:
            if(ChessGame.P1Color == 'black'):
                self.P2WhiteB.state(['!disabled'])
            else:
                self.P2BlackB.state(['!disabled'])
            ChessGame.P2Color = ""

        print('Player 1 color picked: {}'.format(ChessGame.P1Color))
        print('Player 2 color picked: {}'.format(ChessGame.P2Color))

    def submit(self):
        ChessGame.P1Pass = self.P1PasswordValue.get()
        ChessGame.P2Pass = self.P2PasswordValue.get()
        if(ChessGame.P1Color == "" or ChessGame.P2Color == ""):
            messagebox.showerror(title = "Required Color", message = "One or more player has not selected a COLOR to play as,\nPlease do so to move forward, Thank You!!!")
        elif (ChessGame.P1Pass == "" or ChessGame.P2Pass == ""):
            messagebox.showerror(title = "Required Password", message = "One or more player has not inserted PASSWORD\nPlease do so to move forward, Thank You!!!")
        else:
            ChessGameP1Pass = self.P1PasswordValue.get()
            ChessGame.P2Pass = self.P2PasswordValue.get()

            self.P1PasswordValue.delete(0, END)
            self.P2PasswordValue.delete(0, END)

            print(ChessGame.P1Pass)
            print(ChessGame.P2Pass)
            messagebox.showinfo(title = "Rerouting", message = "Rerouting to the game page, hold tight!!!")

            self.notebook.insert(END, self.gamePage, text = 'Game Page')
            self.notebook.tab(0, state = "hidden")
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
        #print("Map created")

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
       
        #print("X: {}\nY: {}\nColor: {}\nPiece: {}\n".format(x,y,color,piece))
        if(piece == "pawn" or (oldPiece == 'pawn' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_pawn_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_pawn_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                    print(check)
                    if(not check):
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            

        elif(piece == "rook" or (oldPiece == 'rook' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_rook_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_rook_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                    print(check)
                    if(not check):
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            
        elif(piece == "knight" or (oldPiece == 'knight' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_knight_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_knight_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                    print(check)
                    if(not check):
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)


        elif(piece == "bishop" or (oldPiece == 'bishop' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_bishop_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_bishop_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                    print(check)
                    if(not check):
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)

        elif(piece == "queen" or (oldPiece == 'queen' and (piece == 'na' or ((color == 'black' and oldColor == 'white') or (color == 'white' and oldColor == 'black'))))):
            if(ChessGame.state == GameState.WAIT1):
                ChessGame.state = GameState.PLANMOVE1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_queen_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.WAIT2):
                ChessGame.state = GameState.PLANMOVE2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.plan_queen_move(x, y, color)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.PLANMOVE1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.playerTurn(1)
                    ChessGame.state = GameState.WAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                    print(check)
                    if(not check):
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
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
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                    print(check)
                    if(not check):
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)
            elif(ChessGame.state == GameState.INCHECKWAIT1):
                ChessGame.state = GameState.INCHECKPLAN1
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKWAIT2):
                ChessGame.state = GameState.INCHECKPLAN2
                ChessGame.pieceToMove = buttonClicked
                listToEnable = self.modified_plan_move(x, y, color, piece)
                self.disableButtons(listToEnable)
            elif(ChessGame.state == GameState.INCHECKPLAN1):
                if(buttonClicked == ChessGame.pieceToMove):
                    self.checkPlayerTurn(1)
                    ChessGame.state = GameState.INCHECKWAIT1
                elif(buttonClicked != ChessGame.pieceToMove):
                    self.executeMove(buttonClicked)
                    check = self.checkIfCheck('black')
                    if(not check):
                        ChessGame.state = GameState.WAIT2
                        self.playerTurn(2)
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
                        ChessGame.state = GameState.WAIT1
                        self.playerTurn(1)
                    elif(check):
                        ChessGame.state = GameState.INCHECKWAIT1
                        self.checkPlayerTurn(1)

        
    def plan_pawn_move(self, x, y, color):
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




    def plan_rook_move(self, x, y, color, kingCall = False):#4 possible paths which are straight in all directions
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



    def plan_knight_move(self, x, y, color, kingCall = False):
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

    def plan_bishop_move(self, x, y, color, kingCall = False):
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

    def plan_queen_move(self, x, y, color, kingCall = False):
        listToEnable1 = self.plan_rook_move(x, y, color, kingCall)
        listToEnable2 = self.plan_bishop_move(x, y, color, kingCall)
        listToEnable2.pop(0)

        listToEnabel = listToEnable1 + listToEnable2
        return listToEnabel
    
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
            for row in enemyPieces:
                if(row[2] == 'rook'):
                    attackPath = self.plan_rook_move(row[0], row[1], 'black', True)
                    attackPath.pop(0)
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                    #if the rook is in the same row or column as the king then make sure to make it so the king cannot travel backwords as that entire row is in threat
                    if(row[1] == y and row[0] > x and ([x-1,y] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x-1,y]))
                    if(row[1] == y and row[0] < x and ([x+1,y] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x+1,y]))
                    if(row[0] == x and row[1] > y and ([x, y-1] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x,y-1]))
                    if(row[0] == x and row[1] < y and ([x, y+1] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x,y+1]))
                if(row[2] == 'knight'):
                    attackPath = self.plan_knight_move(row[0], row[1], 'black', True)
                    attackPath.pop(0)
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                if(row[2] == 'bishop'):
                    attackPath = self.plan_bishop_move(row[0], row[1], 'black', True)
                    attackPath.pop(0)
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                    #if the bishop is diagnol to the king then the entire diagnol is in threat and the king cannot go backwards on the diagnoal
                    if(x-row[0] < 0 and y-row[1] < 0 and (x-row[0] == y-row[1]) and ([x-1,y-1] in listToEnable)):#if the bishop is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x-1,y-1]))
                    if(x-row[0] > 0 and y-row[1] > 0 and (x-row[0] == y-row[1]) and ([x+1,y+1] in listToEnable)):#if the bishop is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x+1,y+1]))
                    if(row[0]-x > 0 and y-row[1] > 0 and (row[0]-x == y-row[1]) and ([x-1,y+1] in listToEnable)):#if the bishop is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x-1,y+1]))
                    if(row[0]-x < 0 and y-row[1] < 0 and (row[0]-x == y-row[1]) and ([x+1,y-1] in listToEnable)):#if the bishop is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x+1,y-1]))
                if(row[2] == 'queen'):
                    attackPath = self.plan_queen_move(row[0], row[1], 'black', True)
                    attackPath.pop(0)
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                    #if the queen is in the same row or column as the king then make sure to make it so the king cannot travel backwords as that entire row is in threat
                    if(row[1] == y and row[0] > x and ([x-1,y] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x-1,y]))
                    if(row[1] == y and row[0] < x and ([x+1,y] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x+1,y]))
                    if(row[0] == x and row[1] > y and ([x, y-1] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x,y-1]))
                    if(row[0] == x and row[1] < y and ([x, y+1] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x,y+1]))
                    #if the queen is diagnol to the king then the entire diagnol is in threat and the king cannot go backwards on the diagnoal
                    if(x-row[0] < 0 and y-row[1] < 0 and (x-row[0] == y-row[1]) and ([x-1,y-1] in listToEnable)):#if the queen is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x-1,y-1]))
                    if(x-row[0] > 0 and y-row[1] > 0 and (x-row[0] == y-row[1]) and ([x+1,y+1] in listToEnable)):#if the queen is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x+1,y+1]))
                    if(row[0]-x > 0 and y-row[1] > 0 and (row[0]-x == y-row[1]) and ([x-1,y+1] in listToEnable)):#if the queen is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x-1,y+1]))
                    if(row[0]-x < 0 and y-row[1] < 0 and (row[0]-x == y-row[1]) and ([x+1,y-1] in listToEnable)):#if the queen is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x+1,y-1]))
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
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in enemyKingPath) and square != [x,y]):
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                        
                if(row[2] == 'pawn'):
                    if([row[0]-1,row[1]-1] in listToEnable and [row[0]-1,row[1]-1] != [x,y]):
                        listToEnable.pop(listToEnable.index([row[0]-1,row[1]-1]))
                    if([row[0]-1,row[1]+1] in listToEnable and [row[0]-1,row[1]+1] != [x,y]):
                        listToEnable.pop(listToEnable.index([row[0]-1,row[1]+1]))
        elif(color == 'black'):
            enemyPieces = self.pieceFinder('white')
            for row in enemyPieces:
                if(row[2] == 'rook'):
                    attackPath = self.plan_rook_move(row[0], row[1], 'white', True)
                    attackPath.pop(0)
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                    #if the rook is in the same row or column as the king then make sure to make it so the king cannot travel backwords as that entire row is in threat
                    if(row[1] == y and row[0] > x and ([x-1,y] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x-1,y]))
                    if(row[1] == y and row[0] < x and ([x+1,y] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x+1,y]))
                    if(row[0] == x and row[1] > y and ([x, y-1] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x,y-1]))
                    if(row[0] == x and row[1] < y and ([x, y+1] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x,y+1]))
                if(row[2] == 'knight'):
                    attackPath = self.plan_knight_move(row[0], row[1], 'white', True)
                    attackPath.pop(0)
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                if(row[2] == 'bishop'):
                    attackPath = self.plan_bishop_move(row[0], row[1], 'white', True)
                    attackPath.pop(0)
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]):
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                    #if the bishop is diagnol to the king then the entire diagnol is in threat and the king cannot go backwards on the diagnoal
                    if(x-row[0] < 0 and y-row[1] < 0 and (x-row[0] == y-row[1]) and ([x-1,y-1] in listToEnable)):#if the bishop is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x-1,y-1]))
                    if(x-row[0] > 0 and y-row[1] > 0 and (x-row[0] == y-row[1]) and ([x+1,y+1] in listToEnable)):#if the bishop is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x+1,y+1]))
                    if(row[0]-x > 0 and y-row[1] > 0 and (row[0]-x == y-row[1]) and ([x-1,y+1] in listToEnable)):#if the bishop is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x-1,y+1]))
                    if(row[0]-x < 0 and y-row[1] < 0 and (row[0]-x == y-row[1]) and ([x+1,y-1] in listToEnable)):#if the bishop is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x+1,y-1]))
                if(row[2] == 'queen'):
                    attackPath = self.plan_queen_move(row[0], row[1], 'white', True)
                    attackPath.pop(0)
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in attackPath) and square != [x,y]): 
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                    #if the queen is in the same row or column as the king then make sure to make it so the king cannot travel backwords as that entire row is in threat
                    if(row[1] == y and row[0] > x and ([x-1,y] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x-1,y]))
                    if(row[1] == y and row[0] < x and ([x+1,y] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x+1,y]))
                    if(row[0] == x and row[1] > y and ([x, y-1] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x,y-1]))
                    if(row[0] == x and row[1] < y and ([x, y+1] in listToEnable)):
                        listToEnable.pop(listToEnable.index([x,y+1]))
                    #if the queen is diagnol to the king then the entire diagnol is in threat and the king cannot go backwards on the diagnoal
                    if(x-row[0] < 0 and y-row[1] < 0 and (x-row[0] == y-row[1]) and ([x-1,y-1] in listToEnable)):#if the queen is on the same diagnol but lower and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x-1,y-1]))
                    if(x-row[0] > 0 and y-row[1] > 0 and (x-row[0] == y-row[1]) and ([x+1,y+1] in listToEnable)):#if the queen is on the same diagnol but upper and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x+1,y+1]))
                    if(row[0]-x > 0 and y-row[1] > 0 and (row[0]-x == y-row[1]) and ([x-1,y+1] in listToEnable)):#if the queen is on the same diagnol but upper and to the right (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x-1,y+1]))
                    if(row[0]-x < 0 and y-row[1] < 0 and (row[0]-x == y-row[1]) and ([x+1,y-1] in listToEnable)):#if the queen is on the same diagnol but lower and to the left (refer to corrdinate system for easier visualization and clarity on the if condition)
                        listToEnable.pop(listToEnable.index([x+1,y-1]))
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
                    squareToRemove = []
                    for square in listToEnable:
                        if((square in enemyKingPath) and square != [x,y]):
                            squareToRemove.append(square)
                    for square in squareToRemove:
                        listToEnable.pop(listToEnable.index(square))
                if(row[2] == 'pawn'):
                    if([row[0]+1,row[1]-1] in listToEnable and [row[0]+1,row[1]-1] != [x,y]):
                        listToEnable.pop(listToEnable.index([row[0]+1,row[1]-1]))
                    if([row[0]+1,row[1]+1] in listToEnable and [row[0]+1,row[1]+1] != [x,y]):
                        listToEnable.pop(listToEnable.index([row[0]+1,row[1]+1]))

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
            self.GPHeaderTitle.config(text = 'Player 1 Turn')

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
            self.GPHeaderTitle.config(text = 'Player 2 Turn')

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
            print("Player 1 King is at {}_{}".format(newx,newy))
        elif(currentColor == 'black' and currentPiece == 'king'):
            ChessGame.P2KING = location
            print("Player 2 King is at {}_{}".format(newx,newy))
        else:
            pass

        location.config(text = "{}_{}_{}_{}".format(newx,newy,currentColor,currentPiece))
        ChessGame.pieceToMove.config(text = "{}_{}_{}_{}".format(currentx,currenty,'na','na'))

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
                    kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    print([kx,ky])
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
                    kx, ky, kColor, kPiece = ChessGame.P1KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations):
                        piecesThreatning.append([piece[0], piece[1], 'knight', [[int(piece[0]), int(piece[1])],[kx,ky]]])
                if(piece[2] == 'pawn'):
                    attackLocations = self.plan_pawn_move(piece[0], piece[1], 'black')
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
                    kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations):
                        piecesThreatning.append([piece[0], piece[1], 'knight', [[int(piece[0]), int(piece[1])],[kx,ky]]])
                if(piece[2] == 'pawn'):
                    attackLocations = self.plan_pawn_move(piece[0], piece[1], 'white')
                    kx, ky, kColor, kPiece = ChessGame.P2KING.cget('text').split('_')
                    kx = int(kx)
                    ky = int(ky)
                    if([kx,ky] in attackLocations):
                        piecesThreatning.append([piece[0], piece[1], 'pawn', [[int(piece[0]), int(piece[1])],[kx,ky]]])
                if(piece[2] == 'king'):
                    pass
        
        return piecesThreatning
    
    def moveablePieces(self, color, piecesThreatning):#returns a list of pieces that can attack currently
        print('In Moveable Pieces')
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
            elif(piece[2] == 'bishop'):
                possibleSquare = self.plan_bishop_move(piece[0], piece[1], color)
            elif(piece[2] == 'knight'):
                possibleSquare = self.plan_knight_move(piece[0], piece[1], color)
            elif(piece[2] == 'queen'):
                possibleSquare = self.plan_queen_move(piece[0], piece[1], color)
            elif(piece[2] == 'pawn'):
                possibleSquare = self.plan_pawn_move(piece[0], piece[1], color)
            elif(piece[2] == 'king'):
                possibleSquare = self.plan_king_move(piece[0], piece[1], color)
            
            for square in possibleSquare:
                for location in piecesThreatning:
                    if ([square[0], square[1]] in location[3]):
                        print("Square in question: [{},{}]".format(square[0], square[1]))
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
        print('Game Ended')
        if(player == 'white'):
            messagebox.showinfo(title = "Winner", message = "Congratulations Player 1 has won by checkmate")
        elif(player == 'black'):
             messagebox.showinfo(title = "Winner", message = "Congratulations Player 2 has won by checkmate")
        elif(player == 'stalemate'):
             messagebox.showinfo(title = "Tie", message = "Due to stalemate this is a tie")

    def checkStalemate(self, color):
        pass

    def addImages(self):
        self.W_Pawn = PhotoImage(file = 'ChessGame/Pieces/W_Pawn.gif')
        self.W_Rook = PhotoImage(file = 'ChessGame/Pieces/W_Rook.gif')
        self.W_Knight = PhotoImage(file = 'ChessGame/Pieces/W_Knight.gif')
        self.W_Bishop = PhotoImage(file = 'ChessGame/Pieces/W_Bishop.gif')
        self.W_Queen = PhotoImage(file = 'ChessGame/Pieces/W_Queen.gif')
        self.W_King = PhotoImage(file = 'ChessGame/Pieces/W_King.gif')

        self.B_Pawn = PhotoImage(file = 'ChessGame/Pieces/B_Pawn.gif')
        self.B_Rook = PhotoImage(file = 'ChessGame/Pieces/B_Rook.gif')
        self.B_Knight = PhotoImage(file = 'ChessGame/Pieces/B_Knight.gif')
        self.B_Bishop = PhotoImage(file = 'ChessGame/Pieces/B_Bishop.gif')
        self.B_Queen = PhotoImage(file = 'ChessGame/Pieces/B_Queen.gif')
        self.B_King = PhotoImage(file = 'ChessGame/Pieces/B_King.gif')

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
def main():
    root = Tk()
    chess = ChessGame(root)
    root.mainloop()


if __name__ == "__main__": main()