# Name: Eric Azevedo
# OSU Email: azevedoe@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/06/24
# Description: Implements an optimized HashMap class. Uses a dynamic array to store hash table and 
    # implement chaining for collision resolution using a singly linked list. Average case 
    # performance of all operations must be kept to O(1) time complexity. Chains of key/value pairs 
    # must be stored in linked list nodes. 


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists in the hash map, its associated value must 
        be replaced with the new value. If the given key is not in the hash map, a new key/value pair must be added. When put() is called, 
        if the current load factor of the table is greater than or equal to 1.0, the table must be resized to double its current capacity.
        Uses resize_table() to do this.  
        """

        # assigns HashMap capacity to m and gets the table load through the method and assgins it to 𝝺
        m = self.get_capacity()
        𝝺 = self.table_load()

        # resize the HashMap through resize_table method by doubling the capacity 
        # and sets the new capacity to m if the table load is greater than or equal to 1 
        if 𝝺 >= 1.0:
            self.resize_table(m * 2)
            m = self.get_capacity()
        
        # creates a hash from the key and getting its index by dividing hash by the capacity 
        hash = self._hash_function(key)
        index = hash % m 

        # gets the key/value from the given index 
        key_val = self._buckets.get_at_index(index)

        # if the the key already exist in the index, then it will add the new value to that key and return.
        # if not, then it will insert that key and value and increase the size by 1 
        for i in key_val:
            if i.key == key:
                i.value = value    
                return
        key_val.insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All existing key/value pairs must be put into the new table, meaning the hash table 
        links must be rehashed. Will use put(). First check that new_capacity is not less than 1; if so, the method does nothing. If 
        new_capacity is 1 or more, it makes sure it is a prime number. If not, change it to the next highest prime number. Uses the 
        methods _is_prime() and _next_prime().
        """

        # if the new capacity is less than 1, then it will return
        if new_capacity < 1:
            return
        
        # if the new capacity is not a prime number, then it will get the next closest prime number and make that the new capacity 
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # copy over the table to new table and resets the HashMap
        new_table = self._buckets
        self._buckets = DynamicArray()
        self._size = 0
        self._capacity = new_capacity

        # assign empty Linked Lists 
        for i in range(new_capacity):
            self._buckets.append(LinkedList())

        # assigns length of new table 
        length = new_table.length()

        # for each index, the key and value from the new_table will be added to the HashMap's table 
        for i in range(length):
            key_val = new_table.get_at_index(i)
            for j in key_val:
                self.put(j.key, j.value)

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """

        # assigns the capacity and the size and divides size/capacity to get load factor; return 
        m = self.get_capacity()
        n = self.get_size()
        𝝺 = n / m 
        
        return 𝝺

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """

        # gets capacity and sets empty variable to 0
        m = self.get_capacity()
        empty = 0

        # going through each index of HashMap, if the bucket size is 0, then it will add 1 to empty. 
        # Once it goes through each index, return empty
        for i in range(m):
            var = self._buckets.get_at_index(i)
            if var.length() == 0:
                empty += 1

        return empty 

    def get(self, key: str):
        """
        Returns the value associated with the given key. If the key is not in the hash map, returns None.
        """

        # gets capacity, hash the key, and get the index from that hash
        m = self.get_capacity()
        hash = self._hash_function(key)
        index = hash % m 

        # will get the key/value at that index 
        key_val = self._buckets.get_at_index(index)

        # going though the key/val, if the keys are the same, then it returns the value. Else, returns None
        for i in key_val:
            if i.key == key:
                return i.value 
            
        return None
        
    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise returns False. An empty hash map does not contain any keys.
        """

        # gets capacity, hash the key, and get the index from that hash
        m = self.get_capacity()
        hash = self._hash_function(key)
        index = hash % m 

        # will get the key/value at that index 
        key_val = self._buckets.get_at_index(index)

        # going though the index, if the keys are the same, then it returns True. Else, returns False
        for i in key_val:
            if i.key == key:
                return True
        
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key is not in the hash map, does nothing.
        """

        # gets capacity
        m = self.get_capacity()

        # going though each index in HashMap, gets the key/value and if the keys are the same, removes it and lowers size by 1 
        for i in range(m):
            key_val = self._buckets.get_at_index(i)
            for j in key_val:
                if j.key == key:
                    key_val.remove(key)
                    self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. 
        """

        # gets capacity and creates an array 
        m = self.get_capacity()
        array = DynamicArray()

        # going though the indexs of HashMap, if there is a key/value, it will add them to the array. 
        # Once it goes through the inedexs, return array 
        for i in range(m):
            key_val = self._buckets.get_at_index(i)
            if key_val.length() != 0:
                h = key_val._head
                while h is not None:
                    val = h.key, h.value
                    array.append(val)
                    h = h.next
        
        return array 

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity.
        """

        # gets capacity
        m = self.get_capacity()

        # going though the HashMap, it will replace the bucket with empty linked list. Once that is done, set size to 0 
        for i in range(m):
            self._buckets[i] = LinkedList()
        
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    A standalone function outside of the HashMap class that receives a dynamic array, which is not guaranteed to be sorted. Will return a 
    tuple containing, in this order, a dynamic array comprising the mode (most occurring) value(s) of the given array, and an integer 
    representing the highest frequency of occurrence for the mode value(s). If there is more than one value with the highest frequency, all 
    values at that frequency should be included in the array being returned (the order does not matter). If there is only one mode, the 
    dynamic array will only contain that value. You may assume that the input array will contain at least one element, and that all values
    stored in the array will be strings. You do not need to write checks for these conditions. Must be implemented with O(N) time complexity. 
    For best results, we recommend using the separate chaining hash map instance provided for you in the function's skeleton code.
    """

    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    
    # assigns length of dynamic array and capacity of map 
    length = da.length()
    m = map.get_capacity()

    # going through each index in array to count the frequency of each element. 
    # check if map's table load is >= 1; if so, it will resize map.
    for i in range(length):
        if map.table_load() >= 1.0:
            map.resize_table(m * 2)
        # will get value at i index of array, will hash out that value
        # will get the index from that, will get the value/key at the index.
        da_val = da.get_at_index(i)
        hash = map._hash_function(da_val)
        index = hash % m
        map_key_val = map._buckets.get_at_index(index)

        # if the key in map == value of array, then add 1 to the value in map
        for j in map_key_val:
            if j.key == da_val:
                j.value += 1
                break
        # else, will insert the value of array as key, and 1 as value, to map; increase size of map by 1 
        else:
            map_key_val.insert(da_val, 1)
            map._size += 1

    # create a new array and assign max frequency and max value to None 
    array = DynamicArray()
    max_freq = None
    max_val = None

    # going through the indexes of the original array to find the max frequency and the max value. 
    # will get the array value at the given index. will hash that value. will get the index from the hash value. 
    # will get the key/val from that index in map. will assign the head (where key/val is stored) as h.    
    for i in range(length):
        da_val = da.get_at_index(i)
        hash = map._hash_function(da_val)
        index = hash % m
        map_key_val = map._buckets.get_at_index(index)
        h = map_key_val._head

        # if h has a key/val:
        if h is not None:
            # if max freq/max val has not been assigned: assign val as max freq, assign key as max value, add max value to new array, and assign h as h.next
            if max_freq is None and max_val is None:
                max_freq = h.value
                max_val = h.key
                array.append(max_val)
                h = h.next

            # if max freq/max value has been assigned: going through the index until h is None:
            while h is not None:
                # if value > max freq, then assign val as max freq, assign key as max value, recreate new array, and add max value to array
                if h.value > max_freq:
                    max_val = h.key
                    max_freq = h.value
                    array = DynamicArray()
                    array.append(max_val)

                # if value == max freq, add key to new array
                if h.value == max_freq:
                    array.append(h.key)
                # assign h.next as h to move onto next key/val in index 
                h = h.next 

    # create another array and assign the previous array length 
    array_1 = DynamicArray()
    length = array.length()

    # going through the indexes in the previous array: get the val at the given index and get the length of the newly created array 
    for i in range(length):
        array_val = array.get_at_index(i)
        arr_1_len = array_1.length() 

        # going through the indexes of the newly created array: will get the val at the given index
        for j in range(arr_1_len):
            arr_1_val = array_1.get_at_index(j)

            # if that val == previous array val, then it will move onto the next index
            if arr_1_val == array_val:
                break
        # else, it will add the previous array value to newly created array 
        else:
            array_1.append(array_val)
    
    # return newly created array with the most occurring values, and the highest frequency
    return array_1, max_freq

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
