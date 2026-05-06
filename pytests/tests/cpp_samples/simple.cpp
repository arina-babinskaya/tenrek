int add(int a, int b) {
    return a + b;
}

class Point {
private:
    int x;
    int y;

public:
    Point(int x_value, int y_value) : x(x_value), y(y_value) {}

    int getX() const {
        return x;
    }

    int getY() const {
        return y;
    }
};
