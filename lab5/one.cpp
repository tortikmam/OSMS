
#include <iostream>
#include <string>

using namespace std;

string crc(string data, string gen, bool addZeros) {

    if (addZeros)
        data += string(7, '0');

    string temp = data;

    for (int i = 0; i <= (int)temp.size() - (int)gen.size(); i++) {
        if (temp[i] == '1') {
            for (int j = 0; j < (int)gen.size(); j++) {
                if (temp[i + j] == gen[j])
                    temp[i + j] = '0';
                else
                    temp[i + j] = '1';
            }
        }
    }

    return temp.substr(temp.size() - 7);
}

int main() {
    string gen = "11011110";

    // Пакет 30 бит
    string data = "";

    for (int i = 0; i < 30; i++) {
        if (i % 2 == 0)
            data += "1";
        else
            data += "0";
    }

    string code = crc(data, gen, true);
    string packet = data + code;

    cout << "Пакет 30 бит: " << data << endl;
    cout << "CRC: " << code << endl;
    cout << "Проверка: " << crc(packet, gen, false) << endl;

    if (crc(packet, gen, false) == "0000000")
        cout << "Ошибок нет" << endl;
    else
        cout << "Обнаружена ошибка" << endl;

    cout << endl;

    // Пакет 250 бит
    data = "";

    for (int i = 0; i < 250; i++) {
        if (i % 2 == 0)
            data += "1";
        else
            data += "0";
    }

    code = crc(data, gen, true);
    packet = data + code;

    cout << "Пакет 250 бит" << endl;
    cout << "CRC: " << code << endl;

    if (crc(packet, gen, false) == "0000000")
        cout << "Ошибок нет" << endl;
    else
        cout << "Обнаружена ошибка" << endl;

    cout << endl;

    // Проверка каждого бита на ошибку
    int detected = 0;
    int notDetected = 0;

    for (int i = 0; i < (int)packet.size(); i++) {
        if (packet[i] == '0')
            packet[i] = '1';
        else
            packet[i] = '0';

        if (crc(packet, gen, false) != "0000000")
            detected++;
        else
            notDetected++;

        if (packet[i] == '0')
            packet[i] = '1';
        else
            packet[i] = '0';
    }

    cout << "Проверка искажения каждого бита:" << endl;
    cout << "Всего проверок: " << detected + notDetected << endl;
    cout << "Ошибок обнаружено: " << detected << endl;
    cout << "Ошибок не обнаружено: " << notDetected << endl;

    return 0;
}

