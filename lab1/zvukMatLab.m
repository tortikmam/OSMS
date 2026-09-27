[y, Fs] = audioread('golos.wav');


fprintf('Частота дискретизации: %d Гц\n', Fs);

y = y(:, 1); 

dlitelnost = length(y) / Fs; 
fprintf('Длительность записи: %.2f секунд\n', dlitelnost);

Fs_calc = length(y) / dlitelnost; 
fprintf('Вычисленная частота дискретизации: %d Гц\n', Fs_calc);

%проредили  
y_down = downsample(y, 10); 

fprintf('Новая частота дискретизации: %d Гц\n', Fs / 10);

zvuk = audioplayer(y_down, Fs / 10);
disp('Чтобы остановить введи stop(zvuk) в командное окно)');
play(zvuk);
pause(4);

figure;
plot(y_down(1: 5000)); 
title('Амплитуда(5000 отсчетов)');
xlabel('Номер отсчета');
ylabel('Амплитуда');

%% 12


N = 1024; 
x_orig = y(1:N * 10);      
x_down = y_down(1:N);  

X_orig = zeros(1, N * 10);
X_down = zeros(1, N);


for k = 1:(N * 10)
    sum_val = 0; 
    for n = 1:(N * 10)
        sum_val = sum_val + x_orig(n) * exp(-1j * 2 * pi * (k-1) * (n-1) / N);
    end
    X_orig(k) = sum_val;
end


for k = 1:N
    sum_val = 0;
    for n = 1:N
        sum_val = sum_val + x_down(n) * exp(-1j * 2 * pi * (k-1) * (n-1) / N);
    end
    X_down(k) = sum_val;
end


spectrum_orig = abs(X_orig);
spectrum_down = abs(X_down);


f_orig = (0:N-1) * (Fs / N);

f_down = (0:N-1) * ((Fs / 10) / N);

figure;

subplot(2,1,1);
plot(f_orig(1:N/2), spectrum_orig(1:N/2), 'b', 'LineWidth', 1);
title('Амплитудный спектр ориг');
xlabel('Частота (Гц)');
ylabel('Амплитуда');

subplot(2,1,2);
plot(f_down(1:N/2), spectrum_down(1:N/2), 'r', 'LineWidth', 1);
title('Амплитудный спектр прор');
xlabel('Частота (Гц)');
ylabel('Амплитуда');
