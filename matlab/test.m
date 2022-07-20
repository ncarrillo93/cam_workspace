%% IMPORT DATA
clear all;clc
pot_min=40; pot_max=140; path='D:\Escritorio\desarrollo camara\exposicion\';   
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
list_images=dir(strcat(path,num2str(0),'W\','*.bmp'));
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
for pot=pot_min:20:pot_max
    ior_mean=img_mean.(strcat('mean_',num2str(pot))); f = RegresionLineal(exp,ior_mean); rms= 1/size(ior_mean,2)*sum((ior_mean-f).^2);
    plot(exp',ior_mean);
    %legend( strcat( num2str(pot),'W | rms:') , num2str(rms) )
end
hold off
clear pot ior_mean f rms
%f = RegresionLineal(exp_us5,ior_mean5);
%rms = 1/size(ior_mean5,2)*sum((ior_mean5-f).^2);
%%
plot(exp,img_mean.mean_80,exp,RegresionLineal(exp,img_mean.mean_80))