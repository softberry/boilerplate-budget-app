class Category:

    def __init__(self, category):
        self.ledger=[]
        self.total_sum=0
        self.total_spent=0
        self.category = category
        
    
    def title(self):
        result = self.category
        l = (30 - len(self.category) ) / 2
        stars ="".ljust(int(l),"*")
        return stars + result + stars 
    
    def entry(self,i):
        
        amount = " {:.2f}".format(i["amount"])
        description = str(i["description"])

        a = 30 - len(amount) 
        d = description.ljust(30)
        
        return d[0:a]  + amount 

    def entries(self):
        return "\n".join(list(map(self.entry, self.ledger)))

    def __repr__(self):
         return self.title() + "\n" + self.entries()+ "\n" + "Total: " + "{:.2f}".format(self.total_sum)
    
    def deposit(self,amount,description=""):
        self.total_sum += amount
        self.ledger.append({"amount":amount,"description":description})

    def withdraw(self,amount,description=""):
        if(not self.check_funds(amount)):
            return False
        self.total_sum -= amount
        self.total_spent += amount
        self.ledger.append({"amount":amount * -1 ,"description":description})
        return True

    def transfer(self,amount,target):
        if(not self.check_funds(amount)):
            return False
        self.withdraw(amount, "Transfer to " + target.category.capitalize())
        target.deposit(amount, "Transfer from " + self.category.capitalize())
        return True

    def check_funds(self,amount):
        return amount<=self.total_sum
    
    def get_balance(self):
        return self.total_sum
    

def create_spend_chart(categories):
    
    result = "Percentage spent by category\n"
    y_axis = list(range(100,-10,-10))
    
    x_axis = list(map(lambda x:x.category,categories))
    max_len = len(max(x_axis, key=len))
    
    x_labels = list(map(lambda x:"".join([c for c in x.ljust(max_len ," ")]),x_axis))

    vertical_Labels = ""

    for i in range(0,max_len):
        line=""
        eol="\n"

        for n in x_labels:
            line+=" " + n[i:i+1] + " "
            if i + 1 == max_len:
                eol=""
        vertical_Labels+="    " + line + eol
    
    def vis_percent(yVal,val):
        if(yVal<= (val - (val%10))):
            return "o"  
        return ""
    
    
    all_total = sum(list(map(lambda x:x.total_spent,categories)))
    
    
    for i,p in enumerate(y_axis):
        vals = "  ".join(list(map(lambda x:vis_percent(p,x.total_spent / all_total * 100),categories)))
        
        result += str(p).rjust(3," ") + "| " + vals + "\n"

    return result + "    ----------\n" +  vertical_Labels