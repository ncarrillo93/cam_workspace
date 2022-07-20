clc;clear all;
%% import
data40W  = data2struct('D:\Escritorio\desarrollo camara\exposicion\40W\',roi)
data60W  = data2struct('D:\Escritorio\desarrollo camara\exposicion\60W\')
data80W  = data2struct('D:\Escritorio\desarrollo camara\exposicion\80W\')
data100W = data2struct('D:\Escritorio\desarrollo camara\exposicion\100W\')
data120W = data2struct('D:\Escritorio\desarrollo camara\exposicion\120W\')
data140W = data2struct('D:\Escritorio\desarrollo camara\exposicion\140W\')
%%
%% roi mean [116:150],[369:416]
roi40W  = getroi(data40W,[116:150],[369:416])
roi60W  = getroi(data60W,[116:150],[369:416])
roi80W  = getroi(data80W,[116:150],[369:416])
roi100W = getroi(data100W,[116:150],[369:416])
roi120W = getroi(data120W,[116:150],[369:416])
roi140W = getroi(data140W,[116:150],[369:416])
%% Regresiones lineales

time_exp=0:500:29500;
for i=1:5
    aux=RegresionLineal(time_exp,roi140W);
end

hold on
plot(aux,'r')
plot(roi140W,'g')
hold off

%% rms
%% Grafica 2D
%% Grafica 3D

