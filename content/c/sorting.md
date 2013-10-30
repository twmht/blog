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

* Quick Sort，先隨便選一個pivot，小於pivot的放左邊的，大於pivot的放右邊，接著左邊跟右邊又是同樣的子問題，遞迴即可。

        :::C
        void quicksort(int * array,int left,int right){
            if(left >= right)
                return;
            int pivot = array[left];
            int i = left+1;
            int j = right;
            while(true){
                while(i <= right){
                    if(array[i]>pivot)
                        break;
                    i++;
                }
                while(j>left){
                    if(array[j]<pivot)
                        break;
                    j--;
                }
                //現在i的右邊都大於pivot了
                if(i > j)
                    break;
                //大於pivot的放到右邊，小於pivot的放在左邊
                SWAP(array[i],array[j]);
            }
            SWAP(array[left],array[j]);
            //排左邊
            quicksort(array,left,j-1);
            //排右邊
            quicksort(array,j+1,right);
        }

