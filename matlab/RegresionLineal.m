function f = RegresionLineal(x,y)
    [p,a,mu] = polyfit(x,y,2);
    f = polyval(p,x,[],mu);
end