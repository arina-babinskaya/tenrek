#include <iostream>

int foo(int x) {
    if (x > 0) {
        if (x > 2) {
            return x - 1;
        }
        return x;
    }
    return 0;
}

int bar() {
    for (int i = 0; i < 10; i++) {}
    return 1;
}
