Title:定義Comparator
Slug: compator
Category: C/C++
Author: twmht

常見有三種定義方式。

#1. Define operator<()#

    :::cpp-objdump
    struct Edge
    {
        int from, to, weight;
        bool operator<(Edge other) const
        {
            return weight > other.weight;
        }
    };
    void printOut(Edge e){
        printf("%d\n",e.weight);
    }
    vector<Edge> v;
    sort(v.begin(), v.end());
    v.push_back((Edge){1,1,1});
    v.push_back((Edge){1,2,5});
    v.push_back((Edge){1,3,3});
    v.push_back((Edge){1,4,4});
    for_each(v.begin(),v.end(),printOut); //由大到小

#2. Define a custom comparison function#
    :::cpp-objdump
    bool cmp(int a, int b)
    {
        return a < b;
    }
    sort(data.begin(), data.end(), cmp);

#3. Define operator()()#
    :::cpp-objdump
    vector<int> occurrences;
    struct cmp
    {
        bool operator()(int a, int b)
        {
            return occurrences[a] < occurrences[b];
        }
    };
    set<int, cmp> s;
    priority_queue<int, vector<int>, cmp> pq;
