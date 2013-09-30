Title:struct用malloc配置記憶體空間
Slug: C
Date: 2013-09-22 19:19
Category: C
Author: twmht

一個指向struct的指標用動態配置之後,在記憶體裡面是長甚麼樣子?

    :::C
    struct myFtphdr {
            short mf_opcode;
            unsigned short mf_cksum;
            union {
                    unsigned short  mf_block;
                    char mf_filename[1];
            }__attribute__ ((__packed__)) mf_u;
            char mf_data[1];
    }__attribute__ ((__packed__));//告訴編譯器不做最佳化
    printf("%d",sizeof(myFtphdr)) //The size of myFtphdr = 6 bytes 
    //現在配置一個512+6 = 518的記憶體空間給指向myFtphdr的指標
    //但是myFtphdr不是只有六個byte,那剩下的512個byte到哪裡去了?
    struct myFtphdr *packet = (struct myFtphdr*) malloc(512+6);
    //分配512個byte給mf_data,但是mf_data只有一個byte
    fread(packet->mf_data, 1, 512, fin) 
以前一直以為指標指到的struct的size有多少，那麼malloc的空間就該有多少，但這是錯誤的觀念，
給一個簡單的例子:

    :::C
    struct test{
        char a[1];
    };
    struct test *p;
    p = (struct test *)malloc(500);
    strcpy(p->a,"111111111111111111111111111111111111111");
    printf("%s\n",p->a); //剛好是111111111111111111111111111111111111111
原因在於配置記憶體的時候是連續的，以第一個例子來說的話，packet指向一塊配置518個byte的記憶體空間，雖然myFtphdr只有六個byte，但因為是連續的，所以多出來的512個byte都會給mf_data。
