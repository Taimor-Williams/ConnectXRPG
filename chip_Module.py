from enum import Enum

class EnumChips(Enum):
    """
    
    """
    Red = "R"
    Black = 'B'


    def toString():
        """
        
        """

class InterFaceChip:
    """
    AF() = chip placed in connect4 board
    rep invarient:
        true
    protection from rep exposure:
        toString:
            @returns immutable str
    """
    def toString(self)->str:
        """
        @returns chips color
        """

class RedChip(InterFaceChip):
    """
    
    """
    def toString(self) -> str:
        return 'R'
    
    def __str__(self):
        return 'R'
    def __eq__(self, other: InterFaceChip) -> bool:
        return str(self) == str(other)
    
class BlackChip(InterFaceChip):
    """
    
    """ 
    def toString(self) -> str:
        return 'B'
    def __str__(self):
        return 'B'


    
    

