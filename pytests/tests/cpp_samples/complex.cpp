int complex_decision(int x, int y, int z) {
    int result = 0;

    if (x > 0) result++;
    if (x > 10) result++;
    if (y > 0) result++;
    if (y > 10) result++;
    if (z > 0) result++;
    if (z > 10) result++;

    for (int i = 0; i < x; i++) {
        if (i % 2 == 0) {
            result += i;
        } else {
            result -= i;
        }
    }

    while (result < 100) {
        if (result % 3 == 0) {
            result += 5;
        } else if (result % 5 == 0) {
            result += 7;
        } else {
            result++;
        }
    }

    return result;
}
