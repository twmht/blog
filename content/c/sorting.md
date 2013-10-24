Title: sorting
Slug: sort
Category: C/C++
Author: twmht

一些常出現的sorting演算法。有些雖然效率很差，不過面試還滿常問的。

* Bubble sort，把目前在最左邊的值一直往右邊推。

        :::C
        #define SWAP(x,y) int t;t = x;x = y;y = t;
        int main(int argc, char const* argv[])
        {
            int size = 10;
            int ary[10] = {1,3,5,6,2,2,7,1,10,0};
            for(int i = 0;i<size-1;i++){
                bool flag = false;
                for(int j = 0;j<size-1-i;j++){
                    if(ary[j]>ary[j+1]){
                        SWAP(ary[j],ary[j+1]);
                        flag = true;
                    }
                }
                if(!flag){
                    break;
                }
            }
            printf("%d",ary[0]);
            //0 1 1 2 2 3 5 6 7 10
            for(int i = 1;i<size;i++){
                printf(" %d",ary[i]);
            }
            return 0;
        }

* Selection sort, 找第一個最小的，放到左邊的第一個位置，接著找第二個最小的，放到左邊第二個位置...

        :::C
        int main(int argc, char const* argv[])
        {
            int size = 10;
            int ary[10] = {1,3,5,6,2,2,7,1,10,0};
            int mi,m;
            for(int i = 0;i<size-1;i++){
                mi = i;
                for(int j = i+1;j<size;j++)
                    if(ary[j]<ary[mi])
                        mi = j;
                m = ary[mi];
                for(int j = mi;j>i;j--)
                    ary[j] = ary[j-1];

                ary[i] = m;
            }
            printf("%d",ary[0]);
            //0 1 1 2 2 3 5 6 7 10
            for(int i = 1;i<size;i++){
                printf(" %d",ary[i]);
            }
            return 0;
        }

* Insertion Sort，從第二個element開始，看有沒有比前面一個element小，有的話就往前排，接著從第三個element開始...

        :::C
        int main(int argc, char const* argv[])
        {
            int size = 10;
            int ary[10] = {1,3,5,6,2,2,7,1,10,0};
            for(int i = 1;i<size;i++){
                int value = ary[i];
                int j;
                for(j = i-1;j >= 0 && ary[j]>value;j--){
                    ary[j+1] = ary[j];
                }
                ary[j+1] = value;
            }
            printf("%d",ary[0]);
            //0 1 1 2 2 3 5 6 7 10
            for(int i = 1;i<size;i++){
                printf(" %d",ary[i]);
            }
            return 0;
        }

