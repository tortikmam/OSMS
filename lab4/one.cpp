    #include <iostream>

    using namespace std;

    double get_kor(int gl, int sdvig) {
        int matches = 0;
        int mismatches = 0;

        for (int i = 0; i < 31; i++) {
            int bit_original = (gl >> i) & 1;
            int bit_shifted = (gl >> ((i + sdvig) % 31)) & 1;

            if (bit_original == bit_shifted) {
                matches++;
            } else {
                mismatches++;
            }
        }

        return (matches - mismatches) / 31.0;
    }

    double get_cross_kor(int gl, int gl_n, int sdvig) {
        int matches = 0;
        int mismatches = 0;

        for (int i = 0; i < 31; i++) {
            int bit1 = (gl >> i) & 1;
            int bit2 = (gl_n >> ((i + sdvig) % 31)) & 1;

            if (bit1 == bit2) matches++;
            else mismatches++;
        }
        return static_cast<double>(matches - mismatches) / 31.0;
    }

    void print_table(int gl) {
        cout << "Сдвиг | 31 бит последовательности          | Автокорреляция" << endl;
        cout << "------------------------------------------------------------" << endl;

        for (int s = 0; s <= 31; s++) {
            cout << "  " << s << "   | ";

            for (int i = 0; i < 31; i++) {
                int bit = (gl >> ((i + s) % 31)) & 1;
                cout << bit;
            }
            
            cout << " | " << get_kor(gl, s) << endl;
        }
    }

    void print_cross_table(int gl, int gl_n) {

        cout << "Сдвиг | 31 бит последовательности (gl_n) | Взаим. корр." << endl;
        cout << "---------------------------------------------------" << endl;

        for (int s = 0; s <= 31; s++) {
            cout << "  " << s << "   | ";
            for (int i = 0; i < 31; i++) {
                cout << ((gl_n >> ((i + s) % 31)) & 1);
            }
            cout << " | " << get_cross_kor(gl, gl_n, s) << endl;
        }
    }

    void check_balance(int gl) {
        int ones = 0;
        int zeros = 0;

        for (int i = 0; i < 31; i++) {
            if ((gl >> i) & 1)
                ones++;
            else
                zeros++;
        }

        cout << "\nПроверка баланса" << endl;
        cout << "Количество единиц: " << ones << endl;
        cout << "Количество нулей: " << zeros << endl;

        if (abs(ones - zeros) <= 1)
            cout << "Результат: true" << endl;
        else
            cout << "Результат: false" << endl;
    }

    void check_correlation(int gl, double threshold) {
        bool result = true;

        cout << "\nПроверка корреляции" << endl;

        for (int s = 1; s < 31; s++) {
            double kor = get_kor(gl, s);

            if (abs(kor) >= threshold) {
                result = false;
                cout << "Нарушение при сдвиге " << s << ": " << kor << endl;
            }
        }

        cout << "Результат: " << result << endl;
    }

    void check_cycles(int gl) {
        int runs[32] = {0};

        int length = 1;
        int previous = gl & 1;

        for (int i = 1; i < 31; i++) {
            int current = (gl >> i) & 1;

            if (current == previous) {
                length++;
            }
            else {
                runs[length]++;
                length = 1;
                previous = current;
            }
        }

        runs[length]++;

        cout << "\nПроверка цикличности" << endl;

        for (int i = 1; i <= 5; i++) {
            cout << "Циклы длиной " << i << ": "
                << runs[i] << endl;
        }
    }

    int main() {
        int gl = 0;
        int gl_n = 0;
        int mask = 0b11111;

        //int x_b = 0b01010; //10
        //int x_bn = 0b1011; //11
        //int y_b = 0b10001; //17
        //int y_bn = 0b1100; //12

        int x_b  = 0b00001;
        int x_bn = 0b00010;
        int y_b  = 0b00000;
        int y_bn = 0b00000;
        

        for (int i = 0; i < 31; i++) {
            int feedback_y = ((y_b >> 2) & 1) ^ (y_b & 1);
            int feedback_x = ((x_b >> 3) & 1) ^ (x_b & 1);
            int output = (x_b & 1) ^ (y_b & 1);

            gl = (gl << 1) | output;

            x_b = ((x_b >> 1) | (feedback_x << 4)) & mask;
            y_b = ((y_b >> 1) | (feedback_y << 4)) & mask;
        }

        for (int i = 0; i < 31; i++) {
            int feedback_y = ((y_bn >> 2) & 1) ^ (y_bn & 1);
            int feedback_x = ((x_bn >> 3) & 1) ^ (x_bn & 1);
            int output = (x_bn & 1) ^ (y_bn & 1);

            gl_n = (gl_n << 1) | output;

            x_bn = ((x_bn >> 1) | (feedback_x << 4)) & mask;
            y_bn = ((y_bn >> 1) | (feedback_y << 4)) & mask;
        }

        print_table(gl);

        cout << endl;

        print_cross_table(gl, gl_n);

        cout << endl;
        cout << "gl" << endl;
        check_balance(gl);
        check_correlation(gl, 0.3);
        check_cycles(gl);
        cout << endl;
        cout << "gl_n" << endl;
        check_balance(gl_n);
        check_correlation(gl_n, 0.3);
        check_cycles(gl_n);

        return 0;    
    }