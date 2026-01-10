#pragma once
#include <Arduino.h>

class StringSplitter
{
private:
    String *parts;
    int count;

public:
    StringSplitter() : parts(nullptr), count(0) {}

    ~StringSplitter()
    {
        clear();
    }

    void clear()
    {
        if (parts != nullptr)
        {
            delete[] parts;
            parts = nullptr;
        }
        count = 0;
    }

    void split(const String &str, char separator)
    {
        clear();
        int start = 0;
        count = 0;
        parts = new String[1];

        for (int i = 0; i <= str.length(); i++)
        {
            if (i == str.length() || str[i] == separator)
            {
                String *newArr = new String[count + 1];
                for (int j = 0; j < count; j++)
                    newArr[j] = parts[j];
                delete[] parts;
                parts = newArr;

                parts[count++] = str.substring(start, i);
                start = i + 1;
            }
        }
    }

    String get(int index)
    {
        if (index < 0 || index >= count)
            return "";
        return parts[index];
    }

    int size()
    {
        return count;
    }
};