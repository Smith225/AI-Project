#include <iostream>

string retString(string inString)
{
    unordered_set<char> store;
    string result;

    for(int i=0;i<inString.length();i++)
    {
        auto it= store.find(inString[i]);

        // element found
        if(it!= store.end())
        {
            continue;
        }
        else
        {
            store.insert(inString[i]);
            result.push_back(inString[i]);
        }
    }

    return result;
}