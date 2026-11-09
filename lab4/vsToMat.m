
x_b  = 10;
y_b  = 17;

x_bn = 11;
y_bn = 12;

mask = 31;

gl   = zeros(1, 31);
gl_n = zeros(1, 31);

for i = 1:31

    % gl
    fb_x = bitxor(bitget(x_b, 4), bitget(x_b, 1));
    fb_y = bitxor(bitget(y_b, 2), bitget(y_b, 1));

    gl(i) = bitxor(bitget(x_b, 1), bitget(y_b, 1));

    x_b = bitshift(x_b, -1) + fb_x * 16;
    y_b = bitshift(y_b, -1) + fb_y * 16;

    % gl_n
    fb_x = bitxor(bitget(x_bn, 4), bitget(x_bn, 1));
    fb_y = bitxor(bitget(y_bn, 2), bitget(y_bn, 1));

    gl_n(i) = bitxor(bitget(x_bn, 1), bitget(y_bn, 1));

    x_bn = bitshift(x_bn, -1) + fb_x * 16;
    y_bn = bitshift(y_bn, -1) + fb_y * 16;

end

gl   = fliplr(gl);
gl_n = fliplr(gl_n);

% Вывод последовательностей
disp('Первая последовательность:');
disp(gl);

disp('Вторая последовательность:');
disp(gl_n);

gl_bip   = 2 * gl - 1;
gl_n_bip = 2 * gl_n - 1;

% Авто
[acf_xcorr, lags_acf] = xcorr(gl_bip, 'coeff');
acf_auto = autocorr(gl_bip', 'NumLags', 30);

% Взаимная
[ccf_xcorr, lags_ccf] = xcorr(gl_bip, gl_n_bip, 'coeff');

disp('Автокорреляция (xcorr):');
disp([lags_acf(lags_acf >= 0)', acf_xcorr(lags_acf >= 0)']);

disp('Автокорреляция (autocorr):');
disp([(0:30)', acf_auto(:)]);

disp('Взаимная корреляция (xcorr):');
disp([lags_ccf(lags_ccf >= 0)', ccf_xcorr(lags_ccf >= 0)']);

figure;

stem(lags_acf(lags_acf >= 0), acf_xcorr(lags_acf >= 0), 'filled');
hold on;

stem(0:30, acf_auto, 'x');

title('Автокорреляция последовательности gl');
xlabel('Задержка (lag)');
ylabel('Коэффициент корреляции');

legend('xcorr', 'autocorr');
grid on;
xticks(0:5:30);
ylim([-0.5 1.2]);

hold off;
