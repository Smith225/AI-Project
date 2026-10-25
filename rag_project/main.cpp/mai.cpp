#include <iostream>

using namespace std;

int main()
{
    int num;

    // cout << "Enter the no of lines you want to print : " << endl;
    // cin >> num;

    for (int i = 0; i < 10; i = i + 2)
    {
        for (int j = 0; j <= i; j++)
        {
            if (j % 2 == 0)
            {
                cout << "*";
            }
            else
                cout << "_";
        }
        cout << endl;
    }

    return 0;
}