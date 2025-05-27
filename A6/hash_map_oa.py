# Name: Eric Azevedo
# OSU Email: azevedoe@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/06/24
# Description: Implements an optimized HashMap class. Uses a dynamic array to store hash table, and 
    # implement Open Addressing with Quadratic Probing for collision resolution inside that dynamic array. 
    # Key/value pairs must be stored in the array. Average case performance of all operations must be kept 
    # to O(1) time complexity. 

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Updates the key/value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced 
        with the new value. If the given key is not in the hash map, a new key/value pair must be added. When put() is called, if the current
        load factor of the table is greater than or equal to 0.5, the table must be resized to double its current capacity. 
        Uses resize_table() for this. 
        """
        # assigns HashMap capacity to m and gets the table load through the method and assgins it to 𝝺
        m = self.get_capacity()
        𝝺 = self.table_load()

        # resize the HashMap through resize_table method by doubling the capacity 
        # and sets the new capacity to m if the table load is greater than or equal to 0.5
        if 𝝺 >= 0.5:
            self.resize_table(m * 2)
            m = self.get_capacity()
        
        # creates a hash from the key 
        hash = self._hash_function(key)
        
        # sets j to 0 (j will be used to move to next index in quadratic probing)
        j = 0

        # gets index from hash 
        index = (hash + j ** 2) % m

        # get the key/value from the index 
        key_val = self._buckets.get_at_index(index)

        # if there is a key/value at the given index that is not the same key, 
        # will add 1 to j and get the next index, and get the new key/value from that index
        # if keys are the same, will replace the value with new value and return 
        while key_val is not None:
            _TS_ = key_val.is_tombstone
            if _TS_ is True:
                self._buckets.set_at_index(index, HashEntry(key, value))
                self._size += 1
                return
            elif key_val.key == key:
                self._buckets.set_at_index(index, HashEntry(key, value))
                return
            
            j += 1
            next_index = (hash + j**2) % m
            key_val = self._buckets.get_at_index(next_index)
            index = next_index
    
        # if there is a spot open, will insert the key and value and increase size by 1  
        self._buckets.set_at_index(index, HashEntry(key, value))
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All active key/value pairs must be put into the new table, meaning all non-tombstone 
        hash table links must be rehashed. (Hint: consider if any other hash map method we want you to implement would help with this). First
        check that new_capacity is not less than the current number of elements in the hash map; if so, the method does nothing. If 
        new_capacity is valid, make sure it is a prime number; if not, change it to the next highest prime number. You may use the methods 
        _is_prime() and _next_prime() from the skeleton code.
        """

        # assign size of HashMap
        size = self.get_size()

        # if the new capacity is less than size, then it will return
        if new_capacity < size:
            return
        
        # if the new capacity is not a prime number, then it will get the next closest prime number and make that the new capacity 
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # copy over the table to new table and resets the HashMap
        new_buckets = self._buckets
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0
        
        # create None spots 
        for i in range(new_capacity):
            self._buckets.append(None)

        # gets length of original buckets
        length = new_buckets.length()

        # for each index, the key and value from the new_table will be added to the HashMap's table 
        for i in range(length):
            key_val = new_buckets.get_at_index(i)
            if key_val is not None:
                _TS_ = key_val.is_tombstone
                if _TS_ is False:
                    key = key_val.key
                    value = key_val.value
                    self.put(key, value)

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

        # going through each index of HashMap, if value is None or '_TS_', then it will add 1 to empty. 
        # Once it goes through each index, return empty
        for i in range(m):
            var = self._buckets.get_at_index(i)
            if var is None:
                empty += 1
            else:
                _TS_ = var.is_tombstone
                if _TS_ is True:
                    empty += 1

        return empty

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map, returns None.
        """
        # gets capacity
        m = self.get_capacity()

        # going through the hashmap, return value if the key is in the hashmap. Else, return None
        for i in range(m):
            key_val = self._buckets.get_at_index(i)
            if key_val is not None:
                _TS_ = key_val.is_tombstone
                if _TS_ is True:
                    continue
                elif key_val.key == key:
                    return key_val.value
        
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys.
        """
        # gets capacity
        m = self.get_capacity()
        
        # going through the hashmap, return True if the key is in the hashmap. Else, return False 
        for i in range(m):
            key_val = self._buckets.get_at_index(i)
            if key_val is not None:
                _TS_ = key_val.is_tombstone
                if _TS_ is True:
                    continue
                elif key_val.key == key:
                    return True
        
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing 
        (no exception needs to be raised).
        """
        # gets capacity
        m = self.get_capacity()

        # going though each index in HashMap, gets the key/value and if the keys are the same, update tombstone to True and lowers size by 1 
        for i in range(m):
            key_val = self._buckets.get_at_index(i)
            if key_val is not None:
                if key_val.key == key:
                    _TS_ = key_val.is_tombstone
                    if _TS_ is True:
                        continue
                    key_val.is_tombstone = True
                    self._size -= 1
                    return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the 
        dynamic array does not matter.
        """
        # gets capacity and creates an array 
        m = self.get_capacity()
        array = DynamicArray()

        # going though the indexs of HashMap, if there is a key/value, it will add them to the array. 
        # Once it goes through the in\dexs, return array 
        for i in range(m):
            key_val = self._buckets.get_at_index(i)
            if key_val is not None:
                _TS_ = key_val.is_tombstone
                if _TS_ is False:
                    key = key_val.key
                    value = key_val.value
                    array.append((key, value))
        
        return array

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity. 
        """
        # gets capacity
        m = self.get_capacity()

        # going though the HashMap, it will replace the bucket with None. Once that is done, set size to 0 
        for i in range(m):
            self._buckets[i] = None
        
        self._size = 0

    def __iter__(self):
        """
        Enables the hash map to iterate across itself. Initialize a variable to track the iterator's progress 
        through the hash map's contents.
        """
        # sets variable to track index throughout the array 
        self._index = 0
        return self 

    def __next__(self):
        """
        Returns the next item in the hash map, based on the current location of the iterator. It will need to only 
        iterate over active items.
        """

        # gets value through index; if it finds a value that is not None or not '_TS_', will move the index by 1 and return that value
        # will do until it has gone through the array, which it will raise StopIteration 
        try:
            value = self._buckets[self._index]
            while value is None:
                self._index += 1
                value = self._buckets[self._index]
                if value is not None:
                    _TS_ = value.is_tombstone
                    if _TS_ is True:
                        value = None

        except DynamicArrayException:
            raise StopIteration
        
        self._index += 1 
        return value


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
