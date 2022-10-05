NB = 10000; %Number of bins


for x = 1:200
        lam(x) = exp((x-75.0)/10); %Expected rate
        Xarr = 1:NB; %Time bins
        Yarr = randraw('po',lam(x),NB); %Actual Counts
        Earr = sqrt(Yarr); %Errors
        [rate(x), ~] = fminbnd(@(A) flatBG(Xarr,Yarr,Earr,A),0,10*lam(x)); %Fit using Gaussian Cost function
        [ratePo(x),~] = fminbnd(@(A) flatBGpo(Xarr,Yarr,Earr,A),0,10*lam(x)); %Fit using Poisson Cost Function
end
figure;
%Plot differences
diff = lam-rate;
diffPo = lam-ratePo;
ratio = lam./rate;
ratioPo = lam./ratePo;
subplot(2,1,1);
semilogx(lam,diff);
hold on
semilogx(lam,diffPo,'r');
title('Poisson Fit Difference')
xlabel('count rate')
ylabel('count rate - calculated rate');
legend('Least Squares', 'Poisson')
subplot(2,1,2);
semilogx(lam,ratio);
hold on
semilogx(lam,ratioPo,'r');
title('Poisson Fit Ratio')
xlabel('count rate')
ylabel('count rate/calculated rate');
legend('Least Squares', 'Poisson')

