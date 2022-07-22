%% IMPORT DATA
clear all;clc; pot_min=40; pot_max=140; path='D:\Escritorio\desarrollo camara\exposicion\';   
for pot=pot_min:20:pot_max
    for exp=0:500:29500
        strcat(path,num2str(pot),'W\',num2str(exp),'\','*.bmp');
        list_images=dir(strcat(path,num2str(pot),'W\',num2str(exp),'\','*.bmp'));
        list_data=dir(strcat(path,num2str(pot),'W\',num2str(exp),'\','*.json'));
        for i=1:size(list_images,1)
            images_aux(:,:,i)= imread(strcat(path,num2str(pot),'W\',num2str(exp),'\',string(list_images(i).name)));
        end
        images.(strcat('img_',num2str(pot),'W_',num2str(exp),'_us'))=images_aux;
    end
end
list_images=dir(strcat(path,num2str(0),'W\','*.bmp'));q
for i=1:size(list_images,1)
    images_aux(:,:,i)= imread(strcat(path,num2str(0),'W\',string(list_images(i).name)));
end
images.(strcat('img_',num2str(0),'W'))=images_aux;
clear pot exp list_data list_images images_aux i ans path
%% MEAN - Restar offset
offset=mean(images.img_0W,3);
for pot=pot_min:20:pot_max
    for exp=0:500:29500
        img.(strcat('mean_',num2str(pot),'W_',num2str(exp),'_us'))=mean(images.(strcat('img_',num2str(pot),'W_',num2str(exp),'_us')),3)-offset;
    end
end
clear exp pot offset
%% ROI
for pot=pot_min:20:pot_max
    for exp=0:500:29500
        img_roi.(strcat('roi_',num2str(pot),'W_',num2str(exp),'_us'))= images.(strcat('img_',num2str(pot),'W_',num2str(exp),'_us'))([116:164],[370:415]);
    end
end
clear exp pot 
%% MEAN ROI
for pot=pot_min:20:pot_max
    i=1;
    for exp=500:500:29500 %se parte de 500 us. Debido a que el primer valor tiene exposicion automatica
        aux(i)=mean(img_roi.(strcat('roi_',num2str(pot),'W_',num2str(exp),'_us')),'all');
        i=i+1;
    end
    img_mean.(strcat('mean_',num2str(pot)))=aux;
end
clear exp pot aux i
%% Create surface
i=1;
for pot=pot_min:20:pot_max
    sup(:,i)=img_mean.( strcat('mean_',num2str(pot)) );
    i=i+1;
end
surf(sup)
%yticks() %exposicion
clear i pot
%% 
exp=500:500:29500;
hold on
i=1:6

%% Regresión Lineal
hold on
Rl_40W  = RegresionLineal(exp      , img_mean.mean_40       );
Rl_60W  = RegresionLineal(exp(1:23), img_mean.mean_60(1:23) );
Rl_80W  = RegresionLineal(exp(1:11), img_mean.mean_80(1:11) );
Rl_100W = RegresionLineal(exp(1:7) , img_mean.mean_100(1:7) );
Rl_120W = RegresionLineal(exp(1:5) , img_mean.mean_120(1:5) );
Rl_140W = RegresionLineal(exp(1:4) , img_mean.mean_140(1:4) );
%rms = 1/size(ior_mean5,2)*sum((ior_mean5-f).^2);
%%
figure(1); hold on; plot(img_mean.mean_40,'r');plot(Rl_40W,'b'); hold off
figure(2); hold on; plot(img_mean.mean_60(1:23),'r');plot(Rl_60W,'b'); hold off
figure(3); hold on; plot(img_mean.mean_80(1:11),'r');plot(Rl_80W,'b'); hold off
figure(4); hold on; plot(img_mean.mean_100(1:7),'r');plot(Rl_100W,'b'); hold off
figure(5); hold on; plot(img_mean.mean_120(1:5),'r');plot(Rl_120W,'b'); hold off
figure(6); hold on; plot(img_mean.mean_140(1:4),'r');plot(Rl_140W,'b'); hold off
%% RMS
rms(1)= 1/size(img_mean.mean_40,2)*sum((img_mean.mean_40-Rl_40W).^2);
rms(2)= 1/size(img_mean.mean_60(1:23),2)*sum((img_mean.mean_60(1:23)-Rl_60W).^2);
rms(3)= 1/size(img_mean.mean_80(1:11),2)*sum((img_mean.mean_80(1:11)-Rl_80W).^2);
rms(4)= 1/size(img_mean.mean_100(1:7),2)*sum((img_mean.mean_100(1:7)-Rl_100W).^2);
rms(5)= 1/size(img_mean.mean_120(1:5),2)*sum((img_mean.mean_120(1:5)-Rl_120W).^2);
rms(6)= 1/size(img_mean.mean_140(1:4),2)*sum((img_mean.mean_140(1:4)-Rl_140W).^2);
figure
stem(rms)