function [dataStruct]= data2struct (path)
    for exp=0:500:29500
        my_field = strcat('img_',num2str(exp),'k'); 
        [images.(my_field),data.(my_field)] = importarData(strcat(path,num2str(exp),'\')); 
    end
    dataStruct.images=images;
    dataStruct.data=data;
end
