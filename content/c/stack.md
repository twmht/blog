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

用LinkedList實作，以畫圖來看的話，第一個element就是top，這樣較為簡潔。

這個例子還有加入friend class。

    :::cpp-objdump

    #ifndef STACK_H
    #define STACK_H
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    //先宣告Stack的prototype，因為Stack的定義較Node為後，而Node又要先用到Stack。要注意加上template。
    template<typename T>
    class Stack;

    template<typename T>
    class Node{
        public:
            //這個表示Stack是Node的friend，所以Stack可以直接存取Node的private data。
            friend class Stack<T>;
        private:
            Node *next;
            T element;
    };
    template<typename T>
    class Stack{
        public:
        Stack(){
            this->head = NULL;
        }
        Stack(const Stack & other){
            this->head = NULL;
            if(!other.empty()){
                //copy top element
                Node<T> *add = new Node<T>;
                add->element = other.head->element;
                add->next = head;
                this->head = add;
                //copy next element until the end of list
                Node<T> *temp = other.head->next;
                while(temp != NULL){
                    Node<T> *newNode = new Node<T>;
                    newNode->element = temp->element;
                    add->next = newNode;
                    add = newNode;
                    temp = temp->next;
                }

            }
        }
        ~Stack(){
            while(this->head){
                Node<T> *temp = this->head;
                this->head = this->head->next;
                delete temp;
            }
        }

        void push(T s){
            Node<T> *temp;
            temp = new Node<T>;
            temp->element = s;
            temp->next = this->head;
            this->head = temp;
        }

        void pop (){
            if(!empty()){
                Node<T> *temp = this->head;
                this->head = this->head->next;
                delete temp;
            }else{
                fprintf(stderr,"Error: stack empty\n");
            }
                
        }

        int top (){
            if(empty()){
                fprintf(stderr,"Error: stack empty\n");
                return -1;
            }
            return this->head->element;
        }
        //注意，因為copy constructor會呼叫empty，而引數又是constant，所以把empty()設成const function
        bool empty() const{
            return this->head == NULL;
        }
        private:
            //top of the element
            Node<T> *head;

    };
    #endif
