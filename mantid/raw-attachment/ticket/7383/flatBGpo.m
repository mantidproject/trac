function C = flatBGpo(x,y,sig,A)
%Poisson Cost function for flat background
C = 0;
A = A(1);
for i = 1:length(x)
    if sig(i) == 0
        C = C + 2*(A-y(i));
    else
        C = C + 2*((A-y(i))+y(i)*(log(y(i))-log(A)));
    end
end