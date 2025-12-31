class Book:
    def __init__(self, name:str, id:int, total_quantity:int):
        self.name = name
        self.id = id
        self.total_quantity = total_quantity
        self.total_borrowed = 0

    def borrow(self):
        # checks if there are left books to borrow or not 
        # simply checks its quantity that is in the library now only 
        if self.total_quantity - self.total_borrowed == 0:
            return False
        self.total_borrowed += 1
        return True
     
    def return_copy(self):
        #returning the borrowed book back
        #which is a copy of it
        assert self.total_borrowed > 0
        self.total_borrowed -= 1
    
    def __repr__(self):
        return f"Book name: {self.name:20} - id: {self.id} - total quantity: {self.total_quantity} -"\
                f"total borrowed: {self.total_borrowed}"