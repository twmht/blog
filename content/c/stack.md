Title: stack實作
Slug: stack
Category: C/C++
Author: twmht

加入template的實作。
Stack.h

    :::cpp-objdump
    //ignore header files
    #ifndef STACK_H
    #define STACK_H
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    template<typename T>
    class Stack{
        public:
        Stack(){
            this->size = 0;
            this->capacity = 100;
            this->array = new T[capacity];
        }
        Stack(int c){
            this->size = 0;
            this->capacity = c;
            this->array = new T[capacity];
        }
        Stack(const Stack & other){
            this->size = other.size;
            this->capacity = other.capacity;
            this->array = new T[capacity];
            memcpy(this->array,other.array,this->size);
        }
        ~Stack(){delete [] array;}

        void push(T s){
            if(size<capacity){
                array[size++] = s;
            }
            else{
                fprintf(stderr,"Error: stack full\n");
            }
        }

        void pop (){
            if(size == 0)
                fprintf(stderr,"Error: stack empty\n");
            else
                size--;
                
        }

        int top (){
            if(size == 0){
                fprintf(stderr,"Error: stack empty\n");
                return -1;
            }
            return this->array[size-1];
        }
        bool empty(){
            return size == 0;
        }
        private:
            int capacity;
            int size;
            T *array;

    };
    #endif
