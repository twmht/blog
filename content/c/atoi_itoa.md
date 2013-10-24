Title: atoi及itoa的實作
Slug: atoi_itoa
Category: C/C++
Author: twmht

很簡單但面試似乎很常問，先紀錄一下。

    :::C
    //ignore header files
    int atoi(char *);
    void itoa(int,char *);
    void reverse(char *);
    int main(int argc, char const* argv[])
    {
        char s[] = "12345";
        //string to integer
        int i = atoi(s);
        printf("%d\n",i);
        char *a = (char *)malloc(50);
        //integer to string
        itoa(i,a);
        //12345
        printf("%s\n",a);
        itoa(-i,a);
        //-12345
        printf("%s\n",a);
        return 0;
    }
    int atoi(char *s){
        int sum = 0;
        for(int i = 0;s[i] != '\0';i++){
            //注意要扣掉'0'
            sum = sum*10+s[i]-'0';
        }
        return sum;
    };
    void itoa(int n,char *s){
        int flag = 1;
        if (n<0){
            n = -n;
            flag = 0;
        }
        int i = 0;
        while(n != 0){
            //注意要把'0'加回來
            s[i++] = n%10+'0';
            n = n/10;
        }
        if(!flag)
            s[i++] = '-';
        s[i] = '\0';
        reverse(s);
    }
    void reverse(char *s){
        for(int i = 0,j = strlen(s)-1;i<j;i++,j--){
            int c = s[i];
            s[i] = s[j];
            s[j] = c;
        }
    }
