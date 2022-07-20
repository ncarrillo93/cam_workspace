function [images,data] = importarData(path)
    list_images=dir(strcat(path,'*.bmp'));    
    list_data=dir(strcat(path,'*.json'));
    %images(752,480,size(list_images,1))=0;
    media=0;desv_stdr=0;ganancia_db=0;cuartilSup=0;mediana=0;exposicion_us=0;
    for i=1:size(list_images,1)
        aux= imread(strcat(path,string(list_images(i).name)));
        images(:,:,i)=aux;
        
        fname = strcat(path,list_data(i).name);
        fid = fopen(fname); raw = fread(fid,inf); str = char(raw'); fclose(fid);
        data = jsondecode(str);

        media(i) = data.media;
        desv_stdr(i) = data.Desviaci__nEstandar;
        ganancia_db(i) = data.ganancia_db;
        cuartilSup(i)=data.cuartilSuperior;
        mediana(i) = data.mediana;
        exposicion_us(i)=data.exposicion_us;
    end
    data = struct('media',media,'desv_stdr',desv_stdr,'ganancia_db',ganancia_db,'cuartilSup',cuartilSup,'mediana',mediana,'exposicion_us',exposicion_us);
end