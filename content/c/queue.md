Title: queue實作
Slug: queue
Category: C/C++
Author: twmht

用Array實作queue。

    :::cpp-objdump
    #ifndef QUEUE_H
    #define QUEUE_H
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    template<typename T>
    class Queue{
        public:
        Queue():capacity(100){
            this->head = 0;
            this->tail = 0;
            this->size = 0;
            this->array = new T[capacity];
        }
        Queue(int c){
            this->head = 0;
            this->tail = 0;
            this->size = 0;
            this->capacity = c;
            this->array = new T[capacity];
        }
        Queue(const Queue & other){
            this->head = other.head;
            this->tail = other.tail;
            this->size = other.size;
            this->capacity = other.capacity;
            this->array = new T[capacity];
            memcpy(this->array,other.array,this->capacity);
        }
        ~Queue(){delete [] array;}

        void push(T s){
            if(size != capacity){
                array[(tail%capacity)] = s;
                tail++;
                size++;
            }
            else{
                fprintf(stderr,"Error: queue full\n");
            }
        }

        void pop (){
            if(size == 0){
                fprintf(stderr,"Error: queue empty\n");
            }
            else{
                head++;
                size--;
            }
                
        }

        int top (){
            if(size == 0){
                fprintf(stderr,"Error: queue empty\n");
                return -1;
            }
            return this->array[head%capacity];
        }
        bool empty(){
            return size == 0;
        }
        private:
            int head;
            int tail;
            int capacity;
            int size;
            T *array;

    };
    #endif

用LinkedList實作，較為容易。

    :::cpp-objdump

    #ifndef QUEUE_H
    #define QUEUE_H
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    template<typename T>
    class Queue;

    template<typename T>
    class Node{
        friend class Queue<T>;
        private:
            T element;
            Node *next;
    };

    template<typename T>
    class Queue{
        public:
        Queue(){
            this->head = NULL;
            this->tail = NULL;
        }
        Queue(const Queue & other){
            this->head = NULL;
            this->tail = NULL;
            if(!other.empty()){
                Node<T> *temp = other.head;
                this->head = new Node<T>;
                this->head->element = temp->element;
                this->head->next = NULL;
                this->tail = head;
                temp = temp->next;
                while(temp != NULL){
                    tail->next = new Node<T>;
                    tail->next->element = temp->element;
                    tail = tail->next;
                    temp = temp->next;
                }
                tail->next = NULL;
            }

        }
        ~Queue(){
            while(this->head != NULL){
                Node<T> *temp = head;
                head = head->next;
                delete temp;
            }
        }

        void push(T s){
            Node<T> * temp = new Node<T>;
            temp->element = s;
            temp->next = NULL;
            if(head == NULL){
                head = tail = temp;
            }else{
                this->tail->next = temp;
                this->tail = temp;
            }
        }

        void pop (){
            if(empty()){
                fprintf(stderr,"Error: queue empty\n");
            }
            else{
                Node<T> *tmp = head;
                head = head->next;
                delete tmp;
                if(head == NULL)
                    tail = NULL;
            }
                
        }

        int top (){
            if(empty()){
                fprintf(stderr,"Error: queue empty\n");
                return -1;
            }
            return this->head->element;
        }
        bool empty() const{
            return head == NULL && tail == NULL;
        }
        private:
            Node<T> *head;
            Node<T> *tail;

    };
    #endif

