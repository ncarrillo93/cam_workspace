function [roi]=getroi(struct,x,y)
    aux=0:500:29500;
    for exp=1:length(aux)
        %images.(strcat('roi', num2str(exp),'k')) = mean(struct.images.(strcat('img_',num2str(exp),'k'))(x,y,:),'all');
        roi(exp)=mean(struct.images.(strcat('img_',num2str(aux(exp)),'k'))(x,y,:),'all');
    end
end