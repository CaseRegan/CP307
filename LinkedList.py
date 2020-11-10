class Node:
    def  __init__(self, data):
        self.data = data
        self.previous_node = None;
        self.next_node = None;

    def get_data(self):
        return self.data;

class LinkedList:
    def __init__(self):
        self.size = 0;
        self.firstnode = None;
        self.lastnode = None;

    def get_size(self):
        return self.size;

    def add(self, data):
        newnode = Node(data);
        if self.get_size() == 0:
            self.firstnode = newnode;
            self.lastnode = newnode;
        elif self.get_size() == 1:
            self.lastnode = newnode;
            self.firstnode.next_node = self.lastnode;
            self.lastnode.previous_node = self.firstnode;
        else:
            self.lastnode.next_node = newnode;
            newnode.previous_node = self.lastnode;
            self.lastnode = newnode;
        self.size = self.get_size() + 1;

    def delete(self, index):
        deleted_node = None;
        if self.get_size() == 0:
            raise IndexError("Empty List!");
        elif self.get_size() == 1:
            deleted_node = self.firstnode;
            self.firstnode = None;
            self.lastnode = None;
        elif index == 0:
            deleted_node = self.firstnode;
            self.firstnode = self.firstnode.next_node
        elif index == self.get_size() - 1:
            deleted_node = self.lastnode;
            self.lastnode = self.lastnode.previous_node;
        else:
            currentnode = self.firstnode;
            for i in range(0, index):
                currentnode = currentnode.next_node;
            deleted_node = currentnode;
            currentnode.previous_node.next_node = currentnode.next_node;
            currentnode.next_node.previous_node = currentnode.previous_node;
        self.size = self.get_size() - 1;

        return deleted_node.data;


    def get(self, index):
        if self.get_size() == 0:
            raise IndexError("Empty List!");
        else:
            currentnode = self.firstnode;
            for i in range(0, index):
                currentnode = currentnode.next_node;
            return currentnode.get_data();

def main():
    list = LinkedList();
    list.add(1);
    list.add(2);
    list.add(3);
    print(list.get(0));
    print(list.get(1));
    print(list.get(2));
    print(list.get_size());
    print(list.firstnode.get_data());
    print(list.lastnode.get_data());
    print(list.delete(0));
    print(list.get_size());
    print(list.firstnode.get_data());
    print(list.lastnode.get_data());
    print(list.delete(1));
    print(list.get_size());
    print(list.firstnode.get_data());
    print(list.lastnode.get_data());
    print(list.delete(0));
    print(list.get_size());
    print(list.firstnode);
    print(list.lastnode);
