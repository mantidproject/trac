function C = flatBG(x,y,sig,A)
%Gaussian Cost function for flat background
C = 0;
A = A(1);
for i = 1:length(x)
    if sig(i) == 0
        C = C + (y(i)-A)^2;
    else
        C = C + ((y(i)-A)/sig(i))^2;
    end
end