#welcome to the Supermarket Pathfinder software!
#install libraries
import sqlite3
from tkinter import *
from tkinter import ttk

#connect database
conn = sqlite3.connect('Supermarket Items.db')
cur = conn.cursor()




#manager login screen
def login():
    global password_attempt
    manager_login = Toplevel()
    manager_login.geometry("200x100")
    manager_login.title("Manager Login")
    pass_label = Label(manager_login, text="Password:")
    password_attempt = Entry(manager_login, show="*")
    pass_label.grid(row=0, column=0)
    password_attempt.grid(row=0,column=1)
    login_button = Button(manager_login, text="Login", command=password_check).grid(row=1, column=1)
  



#check that the password entered in the manager login is correct
def password_check():
    password = "WnK2!d"
    p = False
    while p == False:
        if password_attempt.get() == password:
            print("Success")
            p = True
            manager_menu()
        else:
            print("Incorrect.")
            p == False




#manager option menu
def manager_menu():
    manager_menu = Toplevel()
    manager_menu.title("Manager Menu")
    edit_button = Button(manager_menu, text="Edit Item", padx=30, pady=10, command=edit_item).pack()
    add_button = Button(manager_menu, text="Add New Item", padx=30, pady=10, command=add_item).pack()




#edit an item in the database
def edit_item():
    return




#submit a new item to the database
def submit_item():
    #connect database
    conn = sqlite3.connect('Supermarket Items.db')
    cur = conn.cursor()
    
    #submit item details
    cur.execute("INSERT INTO Item VALUES (:item_name, :item_description)")
    
    #commit changes
    conn.commit()
    
    #close database
    conn.close()
    
    #clear input boxes
    item_name.delete(0, END)
    item_description.delete(0, END)
#     item_aisle.delete(0, END)
#     item_bay.delete(0, END)
#     item_shelf.delete(0, END)
#     item_position.delete(0, END)
    return




#interface to add a new item to the database
def add_item():
    global item_name
    global item_description
    global item_aisle
    global item_bay
    global item_shelf
    global item_position
    add_item = Toplevel()
    add_item.title("Add New Item")
    #variables for the inputs
    aisle = StringVar()
    bay = StringVar()
    shelf = StringVar()
    #input boxes
    item_name = Entry(add_item, width=30)
    item_description = Entry(add_item, width=30)
    item_aisle = OptionMenu(add_item, aisle, "1","2","3","4","5")
    item_bay = OptionMenu(add_item, bay, "L1","L2","L3","L4","L5","R1","R2","R3","R4","R5")
    item_shelf = OptionMenu(add_item, shelf, "A","B","C","D","E")
    #labels for the inputs
    name_label = Label(add_item, text="Name:")
    description_label = Label(add_item, text="Description:")
    aisle_label = Label(add_item, text="Aisle number:")
    bay_label = Label(add_item, text="Bay:")
    shelf_label = Label(add_item, text="Shelf number:")
    position_label = Label(add_item, text="Position number:")
    #positioning of widgets
    name_label.grid(row=0,column=0)
    item_name.grid(row=0,column=1)
    description_label.grid(row=1,column=0)
    item_description.grid(row=1,column=1)
    aisle_label.grid(row=2,column=0)
    item_aisle.grid(row=2,column=1)
    bay_label.grid(row=3,column=0)
    item_bay.grid(row=3,column=1)
    shelf_label.grid(row=4,column=0)
    item_shelf.grid(row=4,column=1)
    #submit button to commit changes
    submit_button = Button(add_item, text="Submit Item", padx=30, pady=10, command=submit_item)
    submit_button.grid(row=6,column=1)




def create_list():
    global shopping_list
    #define functions to be used
    
    def update(contents):
        #empty the list
        item_list.delete(0,END)
        #add the items into the list
        for i in contents:
            item_list.insert(END, i)
            
    def update_shopping_list(contents):
        #empty the list
        shopping_list_box.delete(0,END)
        #add the items into the list
        for i in contents:
            shopping_list_box.insert(END, i)
            
    def autofill(event):
        #empty the box
        search.delete(0, END)
        #add the clicked item into the box
        search.insert(0, item_list.get(ACTIVE))
        
    def filter_search(event):
        #get the value in the search box
        searched_for = search.get()
        #if all input is deleted, show the entire list of available items
        if searched_for == "":
            contents = items
        else:
            #loop through the items checking if the searched term is in the list
            contents = []
            for i in items:
                if searched_for.lower() in i.lower():
                    #add any matches to the contents of the on screen list
                    contents.append(i)
        #update the on screen list
        update(contents)
    
    def add_item():
        #add the item selected to the shopping list
        current_item = search.get()
        if current_item in items:
            shopping_list.append(current_item)
            update_shopping_list(shopping_list)
            
        
    #make the window
    customer_menu = Toplevel()
    customer_menu.title("Create Shopping List")
    customer_menu.geometry("400x500")
    label = Label(customer_menu, text="Add items by typing in the box below.")
    label.grid(row=0,column=0)
    shopping_list_label = Label(customer_menu, text="Your List:")
    shopping_list_label.grid(row=3,column=0)
    
    #button to add each item
    add_to_list = Button(customer_menu, text="Add Item", command=add_item)
    add_to_list.grid(row=5,column=0)
    
    #run the pathfinding function
    run_pathfinder = Button(customer_menu, text="Find Route", command=pathfind)
    run_pathfinder.grid(row=6,column=0)
    
    #get the items from the database into a list
    items = []
    cur.execute("SELECT * FROM Item")
    for row in cur.fetchall():
        items.append(row[1])
        
    #search box
    search = Entry(customer_menu)
    search.grid(row=1,column=0)
    
    #On-screen list of all items
    item_list = Listbox(customer_menu, width=50)
    item_list.grid(row=2,column=0)
    
    #Add items to the on-screen list
    update(items)
    
    #autofill feature
    #Create a binding on the item list when an item is clicked
    item_list.bind("<<ListboxSelect>>", autofill)
    
    #Search filter feature
    #Create a binding on the search box
    search.bind("<KeyRelease>", filter_search)
    
    #display the shopping list on screen
    shopping_list = []
    shopping_list_box = Listbox(customer_menu, width=50)
    shopping_list_box.grid(row=4,column=0)
    
 
 
 
#pathfinding function to find the least distance 
def pathfind():
    
    #if there is only one item in the list, do not run the pathfinder
    if len(shopping_list) < 2:
        return shopping_list
    
    #replace all of the item names in shopping list with their IDs
    for i in range(len(shopping_list)):
        current_name = shopping_list[i]
        shopping_list[i] = cur.execute("SELECT ID FROM Item WHERE Name = ?", [current_name])
        
    #create a distance matrix to represent the shopping list
    def create_graph(shopping_list):
        #three lists to store the nodes, their adjacent nodes and the arc weight between each node in the graph
        item_nodes = []
        arc_weights = []
        adjacent_nodes = []
        #loop through the shopping list items, updating the graph with each item and its adjacent nodes
        for i in shopping_list:
            distances = []
            #loop through the items
            for x in range(len(shopping_list)):
                current_node = shopping_list[x]
                #loop through the items adjacent to the current item
                for y in range(len(shopping_list)):
                    next_node = shopping_list[y+1]
                    #get the values of the aisle and bay number from the database
#                     current_aisle = cur.execute("SELECT Aisle FROM Location WHERE ID = SELECT Location_ID FROM Link WHERE Item_ID = ?", (current_node))
#                     current_bay = cur.execute("SELECT Bay FROM Location WHERE ID = SELECT Location_ID FROM Link WHERE Item_ID = ?", (current_node))
#                     next_aisle = cur.execute("SELECT Aisle FROM Location WHERE ID = SELECT Location_ID FROM Link WHERE Item_ID = ?", (next_node))
#                     next_bay = cur.execute("SELECT Bay FROM Location WHERE ID = SELECT Location_ID FROM Link WHERE Item_ID = ?", (next_node))

                    location = cur.execute("SELECT Location_ID FROM Link WHERE Item_ID = ?", [current_node])
                    print(location)

#                     stuff = cur.execute("""SELECT Aisle, Bay FROM Location
#                     WHERE ID = ?""", [location])
#                     print(stuff)
                    #get the bay number from the bay string
                    bay_number = int(current_bay[1])
                    next_bay_number = int(next_bay[1])
                    #calculate the distance between the two items
                    current_position = int(current_aisle) + bay_number
                    next_position = int(next_aisle) + next_bay_number
                    #compare size of position to calculate the positive difference between the items (arc weight)
                    if current_position > next_position:
                        arc_weight = current_position - next_position
                    elif next_position > current_position:
                        arc_weight = next_position - current_position
                    distances.append(arc_weight)
                    adjacents.append(next_node)
            #update graph every time the shopping list is iterated through for the current item
            item_nodes.append(current_node)
            arc_weights.append(distances)
            adjacent_nodes.append(adjacents)
        return item_nodes
        return arc_weights
        return adjacent_nodes
    
    #use prim's algorithm to create a minimum spanning tree
    def prims(item_nodes,arc_weights,adjacent_nodes):
        mst_nodes = [] #stores the nodes in the minimum spanning tree
        mst_dist = [] #stores the distances between the nodes and their adjacent nodes
        mst_adj = [] #stores the nodes adjacent to the node at the same index in the nodes list
        current_node = 0
        for i in item_nodes:
            current_node = item_nodes[i]
            distances = arc_weights[i]
            current_distance = distances[0]
            for x in distances:
                if current_distance <= distances[x]:
                    current_distance = distances[x]
                elif current_distance > distances[x]:
                    current_distance = current_distance
            mst_nodes.append(current_node)
            mst_dist.append(current_distance)
            #find position of lowest distance in order to find the linked node
            adjacent_index = arc_weights.index(current_distance)
            mst_adj.append(adjacent_nodes(adjacent_index))
        return mst_nodes
        return mst_dist
        return mst_adj


    #use the nearest neighbor method to find an upper bound
    def nearest_neighbor(item_nodes,arc_weights,adjacent_nodes):
        return

    items, distances, adjacent_nodes = create_graph(shopping_list)
    #create an empty list for total rmst costs
    rmst_costs = []
    #create an empty list for each element of the mst to be added into
    all_rmst_items = []
    all_rmst_dist = []
    all_rmst_adj = []
    #pop each node in turn and make an RMST using prim's
    for i in shopping_list:
        removed_item = items.pop[i]
        removed_distances = distances.pop[i]
        removed_adjacency = adjacent_nodes.pop[i]
        #make the rmst
        rmst_items, rmst_dist, rmst_adj = prims(items,distances,adjacent_nodes)
        #store each rmst in the lists
        all_rmst_items.append(rmst_items)
        all_rmst_dist.append(rmst_dist)
        all_rmst_adj.append(rmst_adj)
        #calculate the total cost of the rmst without the popped node
        cost = 0
        for distance in rmst_dist:
            cost += distance
        #add the cost of adding the popped node back in by its two shortest distances for the total cost
        for i in range(1):
            cost += min(removed_distances)
            removed_distances.remove(min(removed_distances))
        #add the total cost to the list of costs
        rmst_costs.append(cost)






#interface initialise
window = Tk()
window.title("Supermarket Pathfinder")
window.geometry("200x200")
#initial buttons to call customer and manager functions
customer_button = Button(window, text="Customer", padx=30, pady=10, command=create_list).pack()
manager_button = Button(window, text="Manager", padx=30, pady=10, command=login).pack()



#close database
#conn.close()

mainloop()