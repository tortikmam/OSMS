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
        return (matches - mismatches) / 31.0;
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

    int main() {
        int gl = 0;
        int gl_n = 0;
        int x_b = 0b01010; //10
        int x_bn = 0b1011; //11
        int y_b = 0b10001; //17
        int y_bn = 0b1100; //12
        int mask = 0b11111;

        for (int i = 0; i < 31; i++) {
            int feedback_y = ((y_b >> 1) & 1) ^ (y_b & 1);
            int feedback_x = ((x_b >> 3) & 1) ^ (x_b & 1);
            int output = (x_b & 1) ^ (y_b & 1);

            gl = (gl << 1) | output;

            x_b = ((x_b >> 1) | (feedback_x << 4)) & mask;
            y_b = ((y_b >> 1) | (feedback_y << 4)) & mask;
        }

        for (int i = 0; i < 31; i++) {
            int feedback_y = ((y_bn >> 1) & 1) ^ (y_bn & 1);
            int feedback_x = ((x_bn >> 3) & 1) ^ (x_bn & 1);
            int output = (x_bn & 1) ^ (y_bn & 1);

            gl_n = (gl_n << 1) | output;

            x_bn = ((x_bn >> 1) | (feedback_x << 4)) & mask;
            y_bn = ((y_bn >> 1) | (feedback_y << 4)) & mask;
        }

        print_table(gl);

        cout << endl;

        print_cross_table(gl, gl_n);

        return 0;    
    }